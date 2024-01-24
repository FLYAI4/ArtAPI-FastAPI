import os
import sys
import uvicorn
root_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(root_path, "src"))
apps_path = os.path.abspath(os.path.join(src_path, "apps"))
# libs_path = os.path.abspath(os.path.join(src_path, "libs"))

if src_path not in sys.path:
    sys.path.append(src_path)
if apps_path not in sys.path:
    sys.path.append(apps_path)


if __name__ == "__main__":
    from src.apps import create_app
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
