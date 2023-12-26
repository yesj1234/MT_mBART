from huggingface_hub import snapshot_download
import argparse


def main(args):
    REPO_ID = args.repo_id
    LOCATION_DIR = args.location_dir
    snapshot_download(repo_id = REPO_ID,
                    local_dir_use_symlinks=False,
                    local_dir = LOCATION_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_id", require=True)
    parser.add_argument("--location_dir", require=True)
    args = parser.parse_args()
    main(args)