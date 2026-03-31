from spatialdata.transformations import (
    Affine,
    Scale,
    Sequence,
    Translation,
    BaseTransformation
)

def generate_transformations(
    trans: Optional[list] = None
) -> list[BaseTransformation]:
    
    alltrans = []
    for tr in trans:
        if tr == "translation":
            tr = Translation([10, 20], axes = ("x", "y"))
        elif tr == "scale":
            tr = Scale([0.5, 0.5], axes = ("x", "y"))
        elif tr == "affine":
            tr = Affine(matrix=                [
                    [0.5, 0.2, 0],
                    [0.1, 0.5, 0],
                    [0, 0, 1],
                ], 
                input_axes=("x", "y"), output_axes=("x", "y"))
        else:
            raise ValueError(f"Transformation type '{tr}' not recognized. Please choose from 'translation', 'scale', or 'affine'.")
        alltrans.append(tr)
    
    if(len(alltrans) > 1):
        alltrans = Sequence(alltrans)

    return alltrans
    

    