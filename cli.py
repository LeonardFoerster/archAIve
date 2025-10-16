import argparse
import core
import os
import datetime

def main():
    category_list_string = ""
    current_field = ""
    for name, code in core.ARXIV_CATEGORIES.items():
        field = code.split('.')[0]
        if field != current_field:
            category_list_string += f"\n--- {field.upper()} ---\n"
            current_field = field
        category_list_string += f"  - {name}\n"

    parser = argparse.ArgumentParser(
        usage=argparse.SUPPRESS,
        description="📚 A command-line tool to fetch and summarize the latest papers from arXiv.",
        epilog=f"""
Example Usage:
  python cli.py -c cs.LG -n 5 --outdir ./summaries

Available Categories:{category_list_string}
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-c", "--category", 
        required=True,
        metavar="CATEGORY_CODE",
        help="The required arXiv category code. See the full list below.",
        choices=core.ARXIV_CATEGORIES.values()
    )
    
    parser.add_argument(
        "-n", "--number", 
        type=int, 
        default=3, 
        help="Number of papers to fetch (default: 3)."
    )
    
    parser.add_argument(
        "-o", "--outdir",
        metavar="PATH",
        help="Optional: The directory path where the output .txt file will be saved."
    )
    
    args = parser.parse_args()

    print(f"Fetching {args.number} latest papers for category: {args.category}")
    
    papers = core.fetch_arxiv_papers(category=args.category, max_results=args.number)

    if not papers:
        print("Could not retrieve papers. Exiting.")
        return

    print("\nLoading summarization model... (This may take a moment on first run)")
    summarizer = core.create_summarizer()
    print("Model loaded successfully.\n")

    full_output_string = ""

    for i, paper in enumerate(papers):
        paper_output = (
            f"--- Paper {i+1}/{len(papers)} ---\n"
            f"Title: {paper.title}\n"
            f"Authors: {', '.join(author.name for author in paper.authors)}\n"
            f"Published: {paper.published.split('T')[0]}\n\n"
            "Summarizing abstract...\n"
        )
        
        summary = core.summarize_text(paper.summary, summarizer)
        paper_output += f"Summary: {summary}\n\n"

        print(paper_output)
        
        full_output_string += paper_output

    if args.outdir:
        try:
            os.makedirs(args.outdir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arxiv_{args.category}_{timestamp}.txt"
            filepath = os.path.join(args.outdir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_output_string)
            
            print(f"✅ Success! Output saved to: {filepath}")
        
        except Exception as e:
            print(f"❌ Error: Could not write to file. {e}")

if __name__ == "__main__":
    main()
