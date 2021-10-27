#!/usr/bin/env python3

# GetSubtree.pl
# Subtree finder which extracts a subtree from an Alpino XML tree

# version 1.8 date: 23.05.2018 made more robust for new versions of Alpino
# version 1.7 date: 15.12.2014  bug fix
# version 1.6 date: 15.10.2014  RELEASED WITH GrETEL2.0
# written by Liesbeth Augustinus (c) 2014
# for the GrETEL2.0 project

#########################################################################

# argument: -xml: path to xml-tree (with @interesting attrib in the nodes that should be kept)
# options:
# -r (remove):
#     - rel: remove top rel
#     - cat: remove top cat
#     - relcat: remove top rel and top cat
#
# -m (mode):
#           - alpino (default): rel, cat, pos, root, token, begin
#           - lassy: rel, cat, pos, postag, root, token, begin
#           - cgn: rel, cat, pt, postag, lemma, token, begin
#           - sonar: rel, cat, pt, postag, lemma, token, begin
#
# -split/-s: split extended pos tags

#########################################################################

import sys
import re
from lxml import etree

def get_subtree(twig, options):
    refpos = initialize()

    # start at 'top' node (leave out alpino_ds node, skip 'parser' tag)
    # 1.8 added 'node'restriction to make sure the first_child is the syntax tree
    root = twig.find('node') # start at 'top' node (leave out alpino_ds node)
    tree     = twig.getchildren()[0]
    children = tree.getchildren()
    del children[1]
    subtree = process_twig( root, refpos )
    subtree = cut_unary(subtree)

    # Remove top node attrib
    if options != None:
        top = subtree
        del top.attrib['rel']
        if options == 'relcat' and top.attrib['cat']:
            top.attrib['cat'] = ' '
        
    return subtree

### subroutines ###

def cut_unary(twig):
    children = twig.getchildren()
    if len(children) == 1:
        return cut_unary( children[0] )
    else:
        return twig

def process_twig( twig, refpos ):
    children = twig.getchildren()
    int = set()
    for child in children:
        result = process_twig( child, refpos )
        if result == None:
            twig.remove(child)
        else:
            twig.attrib['interesting'] = 'cat'

    if 'interesting' in twig.attrib \
        and twig.attrib['interesting'] != 'na':
        interesting = twig.attrib['interesting']
        hash        = twig.attrib

        int.add('rel')
        int.add('begin')
        int.add('pt')

        if interesting == 'cat':
            int.add('cat')
        elif interesting == 'postag':
            int.add('postag')
        elif interesting == 'lemma':
            int.add('lemma')
        elif interesting == 'token':
            int.add('lemma')
            int.add('word')
            int.add('caseinsensitive')
        elif interesting == 'not':
            int.add('not')
            twig.attrib['not'] = 'not'

        for key in hash:
            if not key in int:
                del twig.attrib[key]
                
        if 'postag' in twig.attrib:
            cgntag = twig.attrib['postag']    # get CGN postag
                 # split tag into separate attribute-value pairs
            split = split_one_tag( cgntag, refpos )

            if split:
                for s in split:
                    [att, val ] = s.split('|')
                    twig.attrib[att] = val    # add new elements

        return twig
    
    else:
        return None
        

def split_one_tag(tag, refpos):

    # split tag
    # refpos = reference naar hash
    match = re.match( r'(\w+)\((.*?)\)', tag )
    if match:
        pt  = match.groups(1)                # get pt
        pts = match.groups(2)                # get other parts

    # assign attribute to parts
    pts = pts.split(',')    # split parts
    parts = []
    for val in pts:

        if pt != 'BW' or pt != 'TSW' or pt != 'LET':
            feature = refpos[pt]
            att     = feature[val]    # same as $att=$feature->{$val};
        
        else:
            # do nothing if $pt equals BW, TSW or LET
            return None

        attval = att + '|' + val       # combine attribute-value
        parts.append( attval )

    return parts    # return array of attribute-value pairs

def initialize():

    # hashes with value-attribute pairs

    n = {
        'soort' : 'ntype',
        'eigen' : 'ntype',
        'ev'    : 'getal',
        'mv'    : 'getal',
        'basis' : 'graad',
        'dim'   : 'graad',
        'onz'   : 'genus',
        'zijd'  : 'genus',
        'stan'  : 'naamval',
        'gen'   : 'naamval',
        'dat'   : 'naamval'
    }

    adj = {
        'prenom'   : 'positie',
        'nom'      : 'positie',
        'post'     : 'positie',
        'vrij'     : 'positie',
        'basis'    : 'graad',
        'comp'     : 'graad',
        'sup'      : 'graad',
        'dim'      : 'graad',
        'zonder'   : 'buiging',
        'met-e'    : 'buiging',
        'met-s'    : 'buiging',
        'zonder-n' : 'getal-n',
        'mv-n'     : 'getal-n',
        'stan'     : 'naamval',
        'bijz'     : 'naamval'
    }

    ww = {
        'pv'       : 'wvorm',
        'inf'      : 'wvorm',
        'od'       : 'wvorm',
        'vd'       : 'wvorm',
        'tgw'      : 'pvtijd',
        'verl'     : 'pvtijd',
        'conj'     : 'pvtijd',
        'ev'       : 'pvagr',
        'mv'       : 'pvagr',
        'met-t'    : 'pvagr',
        'prenom'   : 'positie',
        'nom'      : 'positie',
        'vrij'     : 'positie',
        'zonder'   : 'buiging',
        'met-e'    : 'buiging',
        'zonder-n' : 'getal-n',
        'mv-n'     : 'getal-n'
    }

    tw = {
        'hoofd'    : 'numtype',
        'rang'     : 'numtype',
        'prenom'   : 'positie',
        'nom'      : 'positie',
        'vrij'     : 'positie',
        'zonder-n' : 'getal-n',
        'mv-n'     : 'getal-n',
        'basis'    : 'graad',
        'dim'      : 'graad',
        'stan'     : 'naamval',
        'bijz'     : 'naamval'
    }

    vnw = {
        'pers'     : 'vwtype',
        'refl'     : 'vwtype',
        'pr'       : 'vwtype',
        'recip'    : 'vwtype',
        'pos'      : 'vwtype',
        'vrag'     : 'vwtype',
        'betr'     : 'vwtype',
        'bez'      : 'vwtype',
        'vb'       : 'vwtype',
        'excl'     : 'vwtype',
        'aanw'     : 'vwtype',
        'onbep'    : 'vwtype',
        'pron'     : 'pdtype',
        'adv-pron' : 'pdtype',
        'det'      : 'pdtype',
        'grad'     : 'pdtype',
        'stan'     : 'naamval',
        'nomin'    : 'naamval',
        'obl'      : 'naamval',
        'gen'      : 'naamval',
        'dat'      : 'naamval',
        'vol'      : 'status',
        'red'      : 'status',
        'nadr'     : 'status',
        '1'        : 'persoon',
        '2'        : 'persoon',
        '2v'       : 'persoon',
        '2b'       : 'persoon',
        '3'        : 'persoon',
        '3p'       : 'persoon',
        '3m'       : 'persoon',
        '3v'       : 'persoon',
        '3o'       : 'persoon',
        'ev'       : 'getal',
        'mv'       : 'getal',
        'getal'    : 'getal',
        'masc'     : 'genus',
        'fem'      : 'genus',
        'onz'      : 'genus',
        'prenom'   : 'positie',
        'nom'      : 'positie',
        'post'     : 'positie',
        'vrij'     : 'positie',
        'zonder'   : 'buiging',
        'met-e'    : 'buiging',
        'met-s'    : 'buiging',
        'agr'      : 'npagr',
        'evon'     : 'npagr',
        'rest'     : 'npagr',
        'evz'      : 'npagr',
        'agr3'     : 'npagr',
        'evmo'     : 'npagr',
        'rest3'    : 'npagr',
        'evf'      : 'npagr',

        #'mv'=> 'npagr',
        'zonder-n' : 'getal-n',
        'mv-n'     : 'getal-n',
        'basis'    : 'graad',
        'comp'     : 'graad',
        'sup'      : 'graad',
        'dim'      : 'graad'
    }

    lid = {
        'bep'   : 'lwtype',
        'onbep' : 'lwtype',
        'stan'  : 'naamval',
        'gen'   : 'naamval',
        'dat'   : 'naamval',
        'agr'   : 'npagr',
        'evon'  : 'npagr',
        'evmo'  : 'npagr',
        'rest'  : 'npagr',
        'rest3' : 'npagr',
        'evf'   : 'npagr',
        'mv'    : 'npagr'
    }

    vz = {
        'init'  : 'vztype',
        'versm' : 'vztype',
        'fin'   : 'vztype'
    }

    vg = {
        'neven' : 'vgtype',
        'onder' : 'vgtype'
    }

    spec = {
        'afgebr'    : 'spectype',
        'onverst'   : 'spectype',
        'vreemd'    : 'spectype',
        'deeleigen' : 'spectype',
        'meta'      : 'spectype',
        'comment'   : 'spectype',
        'achter'    : 'spectype',
        'afk'       : 'spectype',
        'symb'      : 'spectype'
    }

    # hash of hash references
    refpos = {}
    refpos['N']    = n
    refpos['ADJ']  = adj
    refpos['WW']   = ww
    refpos['TW']   = tw
    refpos['VNW']  = vnw
    refpos['LID']  = lid
    refpos['VZ']   = vz
    refpos['VG']   = vg
    refpos['SPEC'] = spec

    return refpos    # {} => hash reference

[inputxml, options] = sys.argv[1:]

twig = etree.fromstring(bytes(inputxml, encoding='utf-8'))
subtree = get_subtree(twig, options)
print(etree.tostring(subtree, pretty_print=True).decode())
