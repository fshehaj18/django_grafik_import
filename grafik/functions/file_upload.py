def handle_uploaded_file(file, filename):
    with open(filename,'wb+') as fd:
        for ch in file.chunks():
            fd.write(ch)