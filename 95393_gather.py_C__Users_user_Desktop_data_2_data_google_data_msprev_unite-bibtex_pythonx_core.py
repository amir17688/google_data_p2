import bibtex
import cache

ENCODING = 'utf-8'

def candidates(bib_files, cache_dir):
    """
    generate the data for Unite sourcee from the bib_files
    :cache_dir: directory where cache files kept
    :bib_files: list of bib files to read
    :returns: sorted list of tuples [(bibtex key, item text), ...]
    """
    # 1. Sanity check:
    # if bib_files incorrectly set to string, add single bib file to list
    if type(bib_files) is str:
        bib_files = [bib_files]
    # 2. Gather the candidates into unite_keyvals and use cache
    # format of unite_keyvals:
    #   { bibtex-key: text-in-unite-list }
    unite_keyvals = dict()
    for bib in bib_files:
        c = cache.Cache(bib, cache_dir)
        try:
            c.read()
        except (cache.NoCache, cache.OutdatedCache):
            c.update(bibtex.parse)
            c.write()
        unite_keyvals.update(c.data)
    # 3. Create list based on bibtex key, case-insensitive
    gathered = [(bibtex_key, text) for bibtex_key, text in
                sorted(unite_keyvals.viewitems(), key=lambda x: x[0].lower())]
    return gathered

def make_vim_commands(gathered, target, prefix, postfix):
    """
    return the vim commands to pass the candidate list to vim
    :gathered: list of tuples generated by `candidate` function
    :target: vim variable to pass the list to
    :prefix: prefix for inserted cite keys
    :postfix: postfix for inserted cite keys
    :returns: list of vim commands to run
    """
    cmd_list = list()
    for item in gathered:
        action_text = prefix + item[0].encode(ENCODING) + postfix
        word = item[1].replace("'", "''").encode(ENCODING)
        cmd = "call add(%s, {'action__text': '%s', 'word': '%s'})" % (
            target, action_text, word)
        cmd_list.append(cmd)
    return cmd_list
