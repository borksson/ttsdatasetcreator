import os
from rich.console import Console

from datetime import datetime


if __name__ == '__main__':
    console = Console()

    # This is executed when run from the command line

    app_folder = os.path.dirname(os.path.realpath(__file__))

    now = datetime.now()
    project_folder = os.path.join(app_folder, 'project_' + now.strftime("%d%m%Y_%H%M%S"))
    console.print("Please select a [red]project folder[/red] (default [i]%s[/i])." % project_folder)
    in_project_folder = input()
    if not in_project_folder:
        in_project_folder = project_folder
    project_folder = in_project_folder
    if not os.path.exists(project_folder):
        os.mkdir(project_folder)
        
    console.print("Project folder is %s" % project_folder)

    project_name = os.path.basename(project_folder)

    console.print("Copying to tmp folder")

    # Check if tmp folder exists
    if os.path.exists(os.path.join(project_folder, 'tmp')):
        os.system("rm -r %s" % os.path.join(project_folder, 'tmp'))

    os.system("cp -r %s %s" % (project_folder, os.path.join(project_folder, 'tmp')))

    console.print("Cleaning csv")

    wav_files = [x for x in os.listdir(os.path.join(project_folder, 'tmp/wavs')) if x.endswith('.wav')]

    print(wav_files)

    csv_data = ''

    with open(os.path.join(project_folder, 'tmp/metadata.csv'), 'r') as f:
        csv_data = f.read()
        csv_data = csv_data.splitlines()
        csv_data = [x for x in csv_data if x.split('|')[0] in wav_files]
        csv_data = '\n'.join(csv_data)

    with open(os.path.join(project_folder, 'tmp/metadata.csv'), 'w') as f:
        f.write(csv_data)

    console.print("Zipping project")


    if not os.path.exists(os.path.join(app_folder, 'zips')):
        os.mkdir(os.path.join(app_folder, 'zips'))

    os.system("zip -r %s %s" % (os.path.join(app_folder, 'zips', project_name + '.zip'), os.path.join(project_folder, 'tmp')))
    
    console.print("Cleaning tmp folder")

    os.system("rm -r %s" % os.path.join(project_folder, 'tmp'))

    console.print("Done")