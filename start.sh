# #!/bin/bash

# Start the backend
gunicorn app:app &

# Navigate to the frontend directory
cd LLM_Proof_Of_Concept

# Ensure dependencies are installed
npm install

# Build the frontend for production.
npm run build

# Start the frontend server
npm run start


echo "Done"