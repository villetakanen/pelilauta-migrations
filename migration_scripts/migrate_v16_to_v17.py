
from utils import initialize_firestore

db = initialize_firestore()

def update_reactions_with_replies(stream_doc_id, stream_ref, reactions_ref):
    """Updates the reactions document with reply IDs from the stream document."""
    replies_ref = stream_ref.document(stream_doc_id).collection('comments')
    
    # Fetch the existing reaction data
    reaction_doc = reactions_ref.document(stream_doc_id).get()
    if not reaction_doc.exists:
        print(f"Reaction document does not exist for stream {stream_doc_id}")
        return

    reaction_data = reaction_doc.to_dict()
    
    for reply_doc in replies_ref.stream():
        reply_id = reply_doc.id

        # Get the existing subscribers, or an empty list if it doesn't exist
        existing_subscribers = reaction_data.get('subscribers', [])

        # Add the reply ID to the subscribers list if it's not already there
        if reply_id not in existing_subscribers:
            existing_subscribers.append(reply_id)
            reaction_data['subscribers'] = existing_subscribers

            # Update the reactions document with the new subscribers
            reactions_ref.document(stream_doc_id).update({'subscribers': existing_subscribers})
            print(f"Added reply {reply_id} to subscribers for stream {stream_doc_id}")


def migrate_stream_to_reactions():
    stream_ref = db.collection('stream')
    reactions_ref = db.collection('reactions')

    for stream_doc in stream_ref.stream():
        stream_data = stream_doc.to_dict()
        owners = stream_data.get('owners', [])  # Get the owners array, default to empty list if missing

        # Create a new document in the 'reactions' collection
        reaction_data = {
            'subscribers': owners  # Set the subscribers to the owners from the stream
        }
        reactions_ref.document(stream_doc.id).set(reaction_data)
        print(f"Add reactions entry for thread {stream_doc.id} with {len(owners)} subscribers")

        update_reactions_with_replies(stream_doc.id, stream_ref, reactions_ref)


def migrate_v16_to_v17():
    migrate_stream_to_reactions()
    # Your other migration logic here
    pass

if __name__ == "__main__":
    migrate_v16_to_v17()