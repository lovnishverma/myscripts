import os
import win32com.client

def convert_pptx_to_pdf(input_folder):
    # Initialize the PowerPoint application
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    
    # Make PowerPoint invisible during conversion
    powerpoint.Visible = 1
    
    # Iterate through all files in the folder
    for file_name in os.listdir(input_folder):
        # Check if the file is a PowerPoint file (.pptx)
        if file_name.endswith('.pptx'):
            pptx_file_path = os.path.join(input_folder, file_name)
            pdf_file_path = os.path.join(input_folder, file_name.replace('.pptx', '.pdf'))
            
            try:
                # Open the PowerPoint presentation
                presentation = powerpoint.Presentations.Open(pptx_file_path)
                
                # Save as PDF
                presentation.SaveAs(pdf_file_path, FileFormat=32)  # 32 corresponds to PDF format
                presentation.Close()
                print(f"Converted {file_name} to PDF successfully!")
            
            except Exception as e:
                print(f"Failed to convert {file_name}: {e}")
    
    # Close PowerPoint application after all conversions
    powerpoint.Quit()

if __name__ == "__main__":
    folder_path = input(print("Enter path of the folder that contains all the ppts"))
    convert_pptx_to_pdf(folder_path)
