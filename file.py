import os

from flask import *
from werkzeug.utils import secure_filename

from models import *
from flask_login import current_user

def _upload_file():

    return render_template('files.html')

def _delete_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if not current_user.is_admin and file.user != current_user:
        return redirect(url_for('no_permission'))
    filename = file.filename
    os.remove("files/" + str(file.id)+'.'+filename.split('.')[-1])
    db.session.delete(file)
    db.session.commit()
    flash('File deleted successfully!', 'success')
    return redirect(url_for('files'))

def _download_file(file_id):
    return send_from_directory("files", file_id)

def _files():
    if request.method == 'POST':
        # 检查是否有文件在表单中
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        # 如果文件名不为空
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            # 保存文件到服务器
            filename = secure_filename(file.filename)
            f = File(filename=filename, user_id=current_user.id, file_path="files/" + filename)
            print(filename.split('.'))
            if filename.split('.')[-1] in ['png', 'jpg', 'jpeg', 'gif']:
                f.filetype="image"
            db.session.add(f)
            db.session.commit()
            file.save(os.path.join("files", str(f.id)+"."+filename.split('.')[-1]))
            flash('File uploaded successfully', 'success')
            return redirect(url_for('files'))
    return render_template("files.html", files=File.query.filter_by(user_id=current_user.id).all())