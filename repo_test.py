from git import Repo
import os

class reg_file:
    def __init__(self):
        #self.path_toSelf = "H:/TestAutoRepo/"  # when we load this on the server this will be fixed
        self.username = "MarcusGenFus"
        self.access_token = "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"
        #self.remote = f"https://{self.username}:{self.access_token}@github.com/GeneralFusion/PIStatusWebApp.git"
        self.remote = f"https://{self.username}:{self.access_token}@https://github.com/MarcusGenFus/TestAutoRepo.git"
        self.repoName = "TestAutoRepo"
        self.branchN = ""
        self.changes_made = []
        self.file = ""
        self.repo = self.get_updated_repo()

    # it should be possible to use the function below as a reset to any changes made in the session
    def get_updated_repo(self):
        tmp_dir = "H:/"
        repo_dir = os.path.join(tmp_dir, self.repoName)
        print(repo_dir)
        if os.path.isdir(repo_dir):
            repo = Repo(repo_dir)
            try:
                repo.git.pull()
            except:
                # This usually means the branch we're on is gone, so just fetch
                repo.git.fetch()
        else:
            os.makedirs(repo_dir)
            repo = Repo.clone_from(self.remote, repo_dir)
        assert not repo.bare
        #return Repo.
        #return Repo.clone_from(self.remote, self.path_toSelf)
        return repo

    def read_last_branch(self):
        curr_dir = os.getcwd() # this will have to be swapped with a static place later
        try:
            with open(curr_dir+"\\last_branch.txt", 'r') as file:
                self.branchN = file.read()
                file.close()
            self.mount_branch(self.branchN)
            return True
        except Exception as e:
            print("Previous version of the last branch could not be found")
            return False

    def write_last_branch(self):
        curr_dir = os.getcwd() # this will have to be swapped with a static place later
        with open(curr_dir + "\\last_branch.txt", 'w+') as file:
            file.write(self.branchN)
            file.close()

    def list_branches(self):
        branch_list = []
        for x in self.repo.heads:
            branch_list.append(x.name)
        return branch_list.copy()

    def mount_branch(self, branchName):
        # this piece of code was created by Ali Esbak modified to fit this implementation
        # Set the branch, first checking to make sure the branch exists on the remote
        remoteBranch = [x for x in self.repo.remote().refs if x.name[7:] == branchName]
        if len(remoteBranch) == 0:
            print([x.name for x in self.repo.remote().refs])
            raise RuntimeError('Remote branch {} not found for {}- make it first then rerun'.format(branchName,
                                                                                                    self.repo.working_tree_dir))
        # Check for local branch, if found check it out and pull to it
        localBranch = [x for x in self.repo.heads if x.name == branchName]
        if len(localBranch) == 1:
            localBranch[0].checkout()
            self.repo.git.pull()
        else:
            # Otherwise, create the local branch
            branch = self.repo.create_head(branchName, remoteBranch[0])
            branch.set_tracking_branch(remoteBranch[0]).checkout()
            self.repo.head.reference = branch
        print("Branch has been mounted")

    def repo_file_checkout(self, filename):
        self.repo_file_release()
        self.file = filename

    def repo_file_release(self):
        # returns the file checked out and references it in sql table
        self.file = ""
        pass

    def update_config(self):
        # this should push a single file to the repo
        # that file should be the file that they checked out
        #self.repo.index.add(f"H:/PIStatusWebApp/WebAppRemoteServer/configs/{self.file}")
        self.repo.index.add(f"H:/TestAutoRepo/files/{self.file}")
        self.repo.index.commit(f"Updating {self.file}")
        origin = self.repo.remote(name="origin")
        origin.push()
