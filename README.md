Task 1: Cloning and Forking
git --version

1. Cloning a Repository:
  - Choose a public GitHub repository of interest (e.g., a project related to your field of study).
      https://github.com/EricGikunguNyokabi/drs
  - Clone the repository to your local machine.
      cd Desktop
      cd drsgit
      git init
      git add .
      eric@eric-HP-2000-Notebook-PC:~/Desktop/drsgit$ git clone https://github.com/EricGikunguNyokabi/drs.git
          Cloning into 'drs'...
          remote: Enumerating objects: 87, done.
          remote: Counting objects: 100% (87/87), done.
          remote: Compressing objects: 100% (87/87), done.
          remote: Total 87 (delta 32), reused 0 (delta 0), pack-reused 0
          Receiving objects: 100% (87/87), 1.26 MiB | 1.94 MiB/s, done.
          Resolving deltas: 100% (32/32), done.

  - Explore the repository's structure, files, and history.
  -       eric@eric-HP-2000-Notebook-PC:~/Desktop/drsgit$ ls
          admin_app.py  drs          drs.sql               __pycache__       templates
          app.py        drs_main.py  egnpythonanywhere.py  requirements.txt
          Blueprint     DRS.odp      env                   sms.py
          co_app.py     DRS.pptx     mpesa.py              static
          eric@eric-HP-2000-Notebook-PC:~/Desktop/drsgit$ ls app.py
          app.py
          eric@eric-HP-2000-Notebook-PC:~/Desktop/drsgit$ cat app.py
          



2. Forking a Repository:

  - Fork the same repository you cloned in Task 1 to your GitHub account.

  - Clone the forked repository to your local machine.



Task 2: Managing Branches

3. Creating and Switching Branches:

  - In your local repository, create a new branch (e.g., `feature-update`).

  - Switch to the newly created branch.



4. Making Changes and Committing:

  - Make changes to a file or add a new file.

  - Commit the changes to the branch.



5. Merging Changes:

  - Switch back to the main branch.

  - Merge the changes from the `feature-update` branch into the main branch.



Task 3: Handling Conflicts

6. Creating Conflicts:

  - In your forked repository, make changes to the same file that you modified in Task 4.

  - Commit the changes.



7. Resolving Conflicts:

  - Create a new branch to resolve the conflict.

  - Resolve the conflict manually in the file.

  - Commit the changes and merge the branch back into `main`.



Task 4: GitHub Pages

8. Enabling GitHub Pages:

  - In your forked repository, create a simple HTML file (e.g., `index.html`).

  - Enable GitHub Pages for the repository and set the source branch to `main`.



9. Accessing the Published Page:

  - Visit the GitHub Pages URL for your repository and verify that the HTML file is accessible online.



Task 5: Open Source Exploration

10. Exploring Open Source Projects:

  - Search for an open-source project on GitHub related to your interests.

  - Explore the project's documentation, issues, and contribution guidelines.



11. Opening an Issue:

  - Open a new issue in the chosen open-source project, suggesting an improvement, reporting a bug, or asking for clarification.



Submission:

- Push all changes to your forked repository on GitHub.

- Share the link to your forked repository and mention the open-source project you explored with the instructor or submit it as per the class instructions.
