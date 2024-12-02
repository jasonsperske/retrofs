import re
import web
from pathlib import Path
import sys

root_path = Path(sys.argv[2]) if len(sys.argv) > 1 else Path.cwd()

urls = (
    '/(.*)', 'Index'
)

render = web.template.render('templates', base='layout')

def sanitize_filename(filename):
    # Get just the filename portion after the last slash
    filename = filename.rsplit('\\', 1)[-1]
    return re.sub(r'[^\w\-_.]', '_', filename)

class Index:
    def GET(self, path=''):
        params = web.input(action=None)
        target_path = root_path / path if path else root_path
        
        if not target_path.exists():
            raise web.notfound()
            
        if target_path.is_dir():
            files = [f for f in target_path.iterdir()]
            render = web.template.render('templates')
            
            if params.action == 'upload':
                return render.upload(current_path=path)
            elif params.action == 'create_dir':
                return render.create_dir(current_path=path)
            return render.listing(files=files, current_path=path)
        else:
            # For files, set the appropriate content type and return the file
            filename = target_path.name
            web.header('Content-Type', 'application/octet-stream')
            web.header('Content-Disposition', f'attachment; filename="{filename}"')
            return open(target_path, 'rb').read()

    def POST(self, path=''):
        target_dir = root_path / path if path else root_path
        
        if not target_dir.exists() or not target_dir.is_dir():
            raise web.notfound()
            
        x = web.input(myfile={})
        if 'myfile' in x:
            safe_filename = sanitize_filename(x.myfile.filename)
            
            filepath = target_dir / safe_filename
            with open(filepath, 'wb') as f:
                f.write(x.myfile.file.read())
        
        raise web.seeother(f'/{path}')  # Redirect back to directory listing

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
