from app.bot.utils import smart_split_message

def test_splitter():
    # Create a long string > 4000 chars
    long_text = "This is a line.\n" * 300  # 16 * 300 = 4800 chars
    
    chunks = smart_split_message(long_text, limit=4000)
    
    print(f"Original length: {len(long_text)}")
    print(f"Number of chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} length: {len(chunk)}")
        if len(chunk) > 4000:
            print(f"❌ Chunk {i+1} is too big!")
            exit(1)
            
    if len(chunks) < 2:
        print("❌ Should have split into at least 2 chunks")
        exit(1)
        
    print("✅ Splitter test passed")

if __name__ == "__main__":
    test_splitter()
