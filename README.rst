python-shogi: a pure Python shogi library
=========================================

.. image:: https://travis-ci.org/gunyarakun/python-shogi.svg
    :target: https://travis-ci.org/gunyarakun/python-shogi

.. image:: https://coveralls.io/repos/gunyarakun/python-shogi/badge.svg
    :target: https://coveralls.io/r/gunyarakun/python-shogi

.. image:: https://landscape.io/github/gunyarakun/python-shogi/prototype/landscape.svg?style=flat
    :target: https://landscape.io/github/gunyarakun/python-shogi

.. image:: https://badge.fury.io/py/python-shogi.svg
    :target: https://pypi.python.org/pypi/python-shogi

Introduction
------------

This is the module for shogi written in Pure Python. It's based on python-chess commit 6203406259504cddf6f271e6a7b1e04ba0c96165.

This is the scholars mate in python-shogi:

.. code:: python

    >>> import shogi

    >>> board = shogi.Board()

    >>> board.push(shogi.Move.from_usi('7g7f'))

    >>> board.push_usi('3c3d')
    Move.from_usi('3c3d')
    >>> board.push_usi('8h2b+')
    Move.from_usi('8h2b+')
    >>> board.push_usi('4a5b')
    Move.from_usi('4a5b')
    >>> board.push_usi('B*4b')
    Move.from_usi('B*4b')
    >>> board.push_usi('5a4a')
    Move.from_usi('5a4a')
    >>> board.push_usi('2b3a')
    Move.from_usi('2b3a')
    >>> board.is_checkmate()
    True

Features
--------

* Supports Python 2.7 and Python 3.3+.

* Supports standard shogi (hon shogi)

* Legal move generator and move validation.

  .. code:: python

      >>> shogi.Move.from_usi("5i5a") in board.legal_moves
      False

* Make and unmake moves.

  .. code:: python

      >>> last_move = board.pop() # Unmake last move
      >>> last_move
      Move.from_usi('2b3a')

      >>> board.push(last_move) # Restore

* Show a simple ASCII board.

  .. code:: python

      >>> print(board)
       l  n  s  g  .  k +B  n  l
       .  r  .  .  g  B  .  .  .
       p  p  p  p  p  p  .  p  p
       .  .  .  .  .  .  p  .  .
       .  .  .  .  .  .  .  .  .
       .  .  P  .  .  .  .  .  .
       P  P  .  P  P  P  P  P  P
       .  .  .  .  .  .  .  R  .
       L  N  S  G  K  G  S  N  L
      <BLANKLINE>
       S*1

* Show a KIF style board.

  .. code:: python

      >>> print(board.kif_str())
      後手の持駒：
        ９ ８ ７ ６ ５ ４ ３ ２ １
      +---------------------------+
      |v香v桂v銀v金 ・v玉 馬v桂v香|一
      | ・v飛 ・ ・v金 角 ・ ・ ・|二
      |v歩v歩v歩v歩v歩v歩 ・v歩v歩|三
      | ・ ・ ・ ・ ・ ・v歩 ・ ・|四
      | ・ ・ ・ ・ ・ ・ ・ ・ ・|五
      | ・ ・ 歩 ・ ・ ・ ・ ・ ・|六
      | 歩 歩 ・ 歩 歩 歩 歩 歩 歩|七
      | ・ ・ ・ ・ ・ ・ ・ 飛 ・|八
      | 香 桂 銀 金 玉 金 銀 桂 香|九
      +---------------------------+
      先手の持駒：　銀

* Detects checkmates, stalemates.

  .. code:: python

      >>> board.is_stalemate()
      False
      >>> board.is_game_over()
      True

* Detects repetitions. Has a half move clock.

  .. code:: python

      >>> board.is_fourfold_repetition()
      False
      >>> board.move_number
      8

* Detects checks and attacks.

  .. code:: python

      >>> board.is_check()
      True
      >>> board.is_attacked_by(shogi.BLACK, shogi.A4)
      True
      >>> attackers = board.attackers(shogi.BLACK, shogi.H5)
      >>> attackers
      SquareSet(0b111000010000000000000000000000000000000000000000000000000000000000000000000000)
      >>> shogi.H2 in attackers
      True
      >>> print(attackers)
      . . . . . . . . .
      . . . . . . . . .
      . . . . . . . . .
      . . . . . . . . .
      . . . . . . . . .
      . . . . . . . . .
      . . . . . . . . .
      . . . . . . . 1 .
      . . . 1 1 1 . . .

* Parses and creates USI representation of moves.

  .. code:: python

      >>> board = shogi.Board()
      >>> shogi.Move(shogi.E2, shogi.E4).usi()
      '2e4e'

* Parses and creates SFENs

  .. code:: python

      >>> board.sfen()
      'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'
      >>> board.piece_at(shogi.I5)
      Piece.from_symbol('K')

* Read and write KIFs.

  .. code:: python

      >>> import shogi.KIF

      >>> kif = shogi.KIF.Parser.parse_file('data/games/habu-fujii-2006.kif')[0]

      >>> kif['names'][shogi.BLACK]
      '羽生善治'
      >>> kif['names'][shogi.WHITE]
      '藤井猛'
      >>> kif['moves'] # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
      ['7g7f',
       '3c3d',
       ...,
       '9a9b',
       '7a7b+']
      >>> kif['win']
      'b'

* Communicate with a CSA protocol.

  Please see `random_csa_tcp_match <https://github.com/gunyarakun/python-shogi/blob/master/scripts/random_csa_tcp_match>`_.

* Parse professional shogi players' name

      >>> import shogi.Person

      >>> shogi.Person.Name.is_professional('羽生　善治 名人・棋聖・王位・王座')
      True

Peformance
----------
python-shogi is not intended to be used by serious shogi engines where
performance is critical. The goal is rather to create a simple and relatively
highlevel library.

You can install the `gmpy2` or `gmpy` (https://code.google.com/p/gmpy/) modules
in order to get a slight performance boost on basic operations like bit scans
and population counts.

python-shogi will only ever import very basic general (non-shogi-related)
operations from native libraries. All logic is pure Python. There will always
be pure Python fallbacks.

Installing
----------

* With pip:

  ::

      sudo pip install python-shogi

* From current source code:

  ::

      python setup.py sdist
      sudo python setup.py install

How to test
-----------

::

  > nosetests
  or
  > python setup.py test # requires python setup.py install

If you want to print lines from the standard output, execute nosetests like following.

::

  > nosetests -s

If you want to test among different Python versions, execute tox.

::

  > pip install tox
  > tox

ToDo
----

- Support USI protocol.

- Support board.generate_attacks() and use it in board.is_attacked_by() and board.attacker_mask().

- Remove rotated bitboards and support `Shatranj-style direct lookup
  <http://arxiv.org/pdf/0704.3773.pdf>`_ like recent python-chess.

- Support %MATTA etc. in CSA TCP Protocol.

- Support board.is_pinned() and board.pin().
