
from utils import initialize_firestore

db = initialize_firestore()

def update_reactions_with_replies(stream_doc_id):
    """Updates the reactions document with reply IDs from the stream document."""
    replies_ref = db.collection('stream').document(stream_doc_id).collection('comments')  

    for reply_doc in replies_ref.stream():
        reply_data = reply_doc.to_dict()
        reply_id = reply_doc.id
        reply_owners = reply_data.get('owners', [])
        reply_lovers = reply_data.get('lovers', [])

        # Update the reactions document with the reply ID and owners
        reactions_ref = db.collection('reactions').document(reply_id)

        reactions_ref.set({
            'entry': 'thread/reply',
            'subscribers': reply_owners,
            'love:': reply_lovers
        }, merge=True)
        print(f"Ractions entry for thread {stream_doc_id} reply {reply_id} with {len(reply_owners)} subscribers")

def migrate_stream_to_reactions():
    stream_ref = db.collection('stream')
    reactions_ref = db.collection('reactions')

    for stream_doc in stream_ref.stream():
        stream_data = stream_doc.to_dict()
        owners = stream_data.get('owners', [])  # Get the owners array, default to empty list if missing

        # Create a new document in the 'reactions' collection
        reaction_data = {
            'entry': 'thread',
            'subscribers': owners  # Set the subscribers to the owners from the stream
        }
        reactions_ref.document(stream_doc.id).set(reaction_data)
        print(f"Add reactions entry for thread {stream_doc.id} with {len(owners)} subscribers")

        update_reactions_with_replies(stream_doc.id)


def migrate_profile_loves_to_reactions():
    """Pulls in the legacy reaction data from profiles, and adds it to the relevant reactions document."""
    profiles_ref = db.collection('profiles')
    reactions_ref = db.collection('reactions')

    for profile_doc in profiles_ref.stream():
        profile_data = profile_doc.to_dict()
        loves = profile_data.get('lovedThreads', [])

        for thread_id in loves:
            profile_id = profile_doc.id

            # Update the reactions document by adding the uid to array 'love'
            reaction_ref = reactions_ref.document(thread_id)

            # IF the document does not exist, it's a deleted thread, so we skip it
            if not reaction_ref.get().exists:
                print(f"Thread {thread_id} does not exist")
                continue

            reaction_data = reaction_ref.get().to_dict()
            love = reaction_data.get('love', [])
            # If the profile ID is not already in the 'love' array, add it
            if profile_id not in love:
                love.append(profile_id)
                reaction_ref.set({
                    'love': love
                }, merge=True)
                print(f"Added profile {profile_id} to love reactions for thread {thread_id}")
            
def migrate_v16_to_v17():
    migrate_stream_to_reactions()
    migrate_profile_loves_to_reactions()
    # Your other migration logic here
    pass

if __name__ == "__main__":
    migrate_v16_to_v17()