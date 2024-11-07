from transformers import pipeline

# Initialize the summarization pipeline with the BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def chunk_text(text, max_tokens=500):
    """Splits text into chunks of up to max_tokens tokens."""
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])


def summarize_text_local(text, max_length=100, min_length=30):
    """
    Summarize long text by chunking if necessary, to create a concise version.

    Args:
        text (str): The text to be summarized.
        max_length (int): The maximum length of the summary for each chunk.
        min_length (int): The minimum length of the summary for each chunk.

    Returns:
        str: A shorter, more concise summary of the text.
    """
    try:
        # Split text into chunks if it is too long
        summaries = []
        for chunk in chunk_text(text):
            summary = summarizer(chunk, max_length=max_length,
                                 min_length=min_length, do_sample=False)[0]['summary_text']
            summaries.append(summary)

        # Combine summaries of all chunks
        combined_summary = " ".join(summaries)

        # Final summary of the combined summaries to make it even more concise
        final_summary = summarizer(combined_summary, max_length=max_length,
                                   min_length=min_length, do_sample=False)[0]['summary_text']
        return final_summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None


# Example usage within this file (can be removed if used as a module)
if __name__ == "__main__":
    # Example of a long extracted text
    extracted_text = """
    Long extracted text from your image, PDF, or DOCX goes here. It may contain multiple paragraphs or pages 
    worth of text that exceeds the model's input limit.
    """
    summary = summarize_text_local(extracted_text)
    print("Summary:\n", summary)
