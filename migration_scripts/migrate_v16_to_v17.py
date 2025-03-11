from google.cloud import firestore

db = firestore.Client()

def migrate_replies_to_reactions(stream_id): 
    stream_ref = db.collection('stream').document(stream_id)
    reactions_ref = db.collection('reactions').document(stream_id)

    for reply_doc in stream_ref.collection('replies').stream():
        reply_data = reply_doc.to_dict()
        owners = reply_data.get('owners', [])  # Get the owners array, default to empty list if missing 

        # Create a new document in the 'reactions' collection
        reaction_data = {
            'subscribers': owners  # Set the subscribers to the owners from the stream
        }
        reactions_ref.document(reply_doc.id).set(reaction_data)
        print(f"Created reactions entry for stream {reply_doc.id} with subscribers: {owners}")

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
        print(f"Created reactions entry for stream {stream_doc.id} with subscribers: {owners}")

        migrate_replies_to_reactions(stream_doc.id)


def migrate_v16_to_v17():
    # Your migration logic here
    migrate_stream_to_reactions()
    pass

if __name__ == "__main__":
    migrate_v16_to_v17()