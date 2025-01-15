import fitz  # PyMuPDF for PDF rendering
import PyPDF2  # For PDF merging
import customtkinter as ctk  # Modern UI Framework
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES  # Drag and Drop support
from PIL import Image, ImageTk  # For PDF thumbnail preview

# Initialize the GUI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Global variables
pdf_file_list = []  # List to hold added PDF files
doc = None  # Active PDF document
thumbnail_image = None  # For displaying thumbnails


# ✅ FUNCTION: Open PDF and Generate Thumbnail
def open_pdf():
    global doc, thumbnail_image
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    try:
        doc = fitz.open(file_path)
        text_output.delete("1.0", ctk.END)
        text_output.insert(ctk.END, f"Opened: {file_path}\nTotal Pages: {len(doc)}\n\n")

        # Generate and display thumbnail preview
        pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        thumbnail_image = ImageTk.PhotoImage(img)
        thumbnail_label.configure(image=thumbnail_image)
        
        # Display the first page's content in the text box
        page = doc.load_page(0)
        text_output.insert(ctk.END, f"\nPage 1 Content:\n{page.get_text()}\n")

        # Add the file to the list for merging later
        if file_path not in pdf_file_list:
            pdf_file_list.append(file_path)
            text_output.insert(ctk.END, f"\nFile Added for Merging: {file_path}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Error opening PDF: {e}")


# ✅ FUNCTION: Merge Multiple PDFs
def merge_pdfs():
    """Merge selected PDF files into a single file."""
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not files:
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not output_path:
        return

    try:
        merger = PyPDF2.PdfMerger()
        for file in files:
            merger.append(file)
        merger.write(output_path)
        merger.close()
        messagebox.showinfo("Success", f"Merged PDFs into {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")


# ✅ FUNCTION: Search Text in the PDF
def search_text():
    global doc
    if not doc:
        messagebox.showwarning("Warning", "Please open a PDF first!")
        return

    search_query = filedialog.askstring("Search PDF", "Enter text to search:")
    if not search_query:
        return

    results = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        if search_query.lower() in page.get_text().lower():
            results.append(f"Page {page_num + 1}")

    if results:
        messagebox.showinfo("Search Results", f'Text found on pages: {", ".join(results)}')
    else:
        messagebox.showinfo("Search Results", "No matches found.")


# ✅ FUNCTION: Drag and Drop Support
def handle_drag_and_drop(event):
    """Handles PDF files dragged into the window."""
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.lower().endswith(".pdf") and file not in pdf_file_list:
            pdf_file_list.append(file)
            text_output.insert(ctk.END, f"\nAdded PDF: {file}\n")


# ✅ GUI SETUP - Main Window
root = TkinterDnD.Tk()
root.title("ProPDF Reader (Uniform Button Colors)")
root.geometry("1000x700")
root.configure(bg="#1b1b1b")  # Custom background color

# ✅ Buttons at the Top
button_frame = ctk.CTkFrame(root, height=50, corner_radius=10, fg_color="#333333")  # Darker top bar
button_frame.pack(side="top", fill="x", padx=10, pady=10)

# Add Buttons to the Top Bar (Uniform Color)
button_color = "#2196f3"  # Light blue color for all buttons
ctk.CTkButton(button_frame, text="Open PDF", command=open_pdf, fg_color=button_color).pack(side="left", padx=10, pady=5)
ctk.CTkButton(button_frame, text="Merge PDFs", command=merge_pdfs, fg_color=button_color).pack(side="left", padx=10, pady=5)
ctk.CTkButton(button_frame, text="Search Text", command=search_text, fg_color=button_color).pack(side="left", padx=10, pady=5)
ctk.CTkButton(button_frame, text="Exit", command=root.quit, fg_color=button_color).pack(side="left", padx=10, pady=5)

# ✅ Thumbnail Section (For PDF Previews)
thumbnail_label = ctk.CTkLabel(root, text="PDF Thumbnail Preview", height=200)
thumbnail_label.pack(pady=20)  # Adjusted padding to move it lower

# ✅ Text Output Section (For PDF Content)
text_output = ctk.CTkTextbox(root, height=350, width=800)
text_output.pack(pady=20)

# ✅ Drag and Drop Configuration
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drag_and_drop)

# ✅ Run the GUI Application
root.mainloop()
