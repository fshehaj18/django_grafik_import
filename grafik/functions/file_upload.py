def handle_uploaded_file(file, filename):
    with open(filename,'wb+') as fd:
        for chu in file.chunks():
            fd.write(chu)