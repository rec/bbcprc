import attr, subprocess


def _git(args):
    cmd = ['git'] + args.split()
    try:
        return subprocess.check_output(cmd).decode('utf8').strip()
    except subprocess.CalledProcessError:
        return ''


@attr.dataclass
class Git:
    branch: str = _git('rev-parse --abbrev-ref HEAD')
    commit_id: str = _git('git log --format=%H -n 1')
    commit_message: str = _git('git log --format=%B -n 1')
