# Page 1 Transcription

(Diagram)
- wrist frame
- object frame
- base_link frame
- Axes labeled x, y, z
- Vectors drawn between object and wrist


1)

a)

^base_link T[:,3] = ^base d


b)

^obj d = ^obj T_head  ^head T_base_link  d

(some crossed-out work above this line)


2)

^wrist T_obj ( ^obj d + ^obj x ) = ^wrist X_obj-axis

where

^wrist T_obj =
^wrist T_base_link
^base_link T_head
^head T_obj


3)

arccos(
(
[0
 0
 1]
·
^wrist X_obj-axis
)
/
(
||[0
   0
   1]||
  ||
^wrist X_obj-axis||
)
)



# Page 2 Transcription

(Origin of wrist frame w.r.t base frame)

1)

^base P_wrist-org = ^base T_wrist[:,3]
(last column = translation)


2)

^head T_obj =

[ 0   0   1   0
 -1   0   0   0
  0  -1   0   0
  0   0   0   1 ]

(reference file)

(Add to TF tree: obj frame as child of head)


^obj T_head  ^head T_base = ^obj P_wrist-org


Origin of wrist frame w.r.t object frame

3)

^obj P_wrist-org + [1
                     0
                     0
                     0]
(to align x-axis)


4)

^wrist T_base
^base T_head
^head T_obj
d_x
=
^wrist d_x

but in code:

^wrist T_base
^base T_head
^head T_obj
d_x
=
^wrist d_x


5)

Display

^wrist d_x
