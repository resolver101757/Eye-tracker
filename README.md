# Eye-tracker


## Description
Simple resnet18 code to train a dodgy eye-tracker. It jumps around a lot, but for purely image input on a relatively small dataset for the task it does a surprisingly good job.

With around 6K samples of me in different lighting conditions, distances, postures, head rotations and offsets, I hit an MSE loss of around 0.0067, which is still an error range of a couple hundred pixels. I noticed a dramatic jump in performance going from 4K samples to 6K, so I definitely think there's plenty more that can be learned with just more samples alone.

Loss dropped to around 0.005 with ~7K samples, but I didn't notice a significant improvement when actually running the model (possibly a dataset issue).

## Possible improvements:
To accurately predict, the model needs to infer info about: - Distance to face - Rotation of head - Rotation of eyes - Head offset - Camera offset and rotation - Screen dimensions

Hopefully by feeding in a few of these features it'll improve convergence time and allow it to track other features better. Tools like dlib facial landmarks could probably be used to track head rotation and offset (in image space), and possibly distance with some maths around distance between features accounting for rotation (no idea what that equation looks like).

To be able to generalize to different setups and people, you'd want to pass in user specific info like display dimensions and camera position & rotation in a configuration step.

Possibly a configuration step could have the user look at five points (centre and corners of monitor), track some features from that like distance and eye + head rotation, and pass that in. I think that would only be effective with a larger dataset of different configurations.
