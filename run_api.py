"""
SceneIQ API Server Runner
Run this script to start the API server with Swagger UI documentation
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("basic_api:app", host="0.0.0.0", port=5000, reload=True)