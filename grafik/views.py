import os
import h5py
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import UploadFileForm
from .functions.file_upload import handle_uploaded_file


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], f"uploaded/{request.FILES['file'].name}")
            return HttpResponseRedirect(f"process-file/{request.FILES['file'].name}")
    else:
        form = UploadFileForm()

    return render(request, "grafik/upload_hdf5.html",{'form':form})

def process_file(request, filename):
    if os.path.isfile(f'uploaded/{filename}'):
        with h5py.File(f'uploaded/{filename}', 'r') as file:
            data = file.keys()
            data_key = request.POST.get('key')
            data_sections = {}
            max_labels = 0 
            if data_key:
                data_points = file[data_key]
                for i, section in enumerate(data_points):
                    data_of_section = list(data_points.get(section))[::120]
                    if len(data_of_section) > max_labels:
                        max_labels = len(data_of_section)
                    data_sections[section] = data_of_section
            
            context = {
                "keys":data,
                "data_sections": data_sections,
                "range": range(max_labels)
            }

            return render(request, "grafik/processed_file.html", context)
    raise Http404()
    