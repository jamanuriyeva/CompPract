import os
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

# Config
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Supabase client setup
sb_client: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def transfer_books(book_id, source_branch, target_branch, amount):
    """Handles book transfer between branches"""
    try:
        print(f"[{datetime.now()}] Transferring {amount} books from {source_branch} to {target_branch}")

        result = sb_client.rpc('move_books_safe', {
            'p_book_id': book_id,
            'p_from_branch_id': source_branch,
            'p_to_branch_id': target_branch,
            'p_quantity': amount
        }).execute()

        if result.data.get('error'):
            print(f"[{datetime.now()}] Failed: {result.data['error']}")
        else:
            print(f"[{datetime.now()}] Successfully moved {amount} books")

    except Exception as err:
        print(f"[{datetime.now()}] Error occurred: {err}")


def run_concurrent_transfer_test():
    """Simulates concurrent book transfers"""
    print("\nRunning lost update simulation...")

    try:
        # Setup test data
        new_book = sb_client.table('books').insert({'name': '1984'}).execute()
        book_id = new_book.data[0]['id']
        
        branches = sb_client.table('branches').insert([
            {'name': 'Main'}, 
            {'name': 'West'}, 
            {'name': 'East'}
        ]).execute()
        branch_ids = [b['id'] for b in branches.data]
        
        sb_client.table('stock').insert({
            'book_id': book_id,
            'branch_id': branch_ids[0],
            'quantity': 10
        }).execute()

        # Run concurrent transfers
        t1 = threading.Thread(
            target=transfer_books,
            args=(book_id, branch_ids[0], branch_ids[1], 5)
        )
        
        t2 = threading.Thread(
            target=transfer_books,
            args=(book_id, branch_ids[0], branch_ids[2], 5)
        )

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Display results
        print("\nCurrent stock:")
        stock_data = sb_client.table('stock').select('*').execute()
        for item in stock_data.data:
            print(f"Book {item['book_id']} at branch {item['branch_id']}: {item['quantity']}")

        print("\nTransfer history:")
        moves = sb_client.table('movements').select('*').execute()
        for move in moves.data:
            print(f"{move['quantity']} books from {move['from_branch_id']} to {move['to_branch_id']}")

    except Exception as e:
        print(f"Setup error: {e}")


if __name__ == "__main__":
    # Clear existing data
    for table in ['movements', 'stock', 'branches', 'books']:
        sb_client.table(table).delete().neq('id', 0).execute()

    run_concurrent_transfer_test()
