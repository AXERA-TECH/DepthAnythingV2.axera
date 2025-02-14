import argparse
import cv2
import numpy as np
from axengine import InferenceSession

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--img",
        type=str,
        required=True,
        help="Path to input image.",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to ONNX model.",
    )
    
    return parser.parse_args()


def infer(img: str, model: str, viz: bool = False):
    img_raw = cv2.imread(img)
    image = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB) 
    orig_h, orig_w = image.shape[:2]
    image = cv2.resize(image, (518,518) )
    image = image[None]

    session = InferenceSession(path_or_bytes=model, providers= ['AxEngineExecutionProvider', 'AXCLRTExecutionProvider'])
    
    depth = session.run(output_names=["output"], input_feed={"input":image})[0]

    depth = cv2.resize(depth[0, 0], (orig_w, orig_h))
    depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
    depth = depth.astype(np.uint8)

    depth_color = cv2.applyColorMap(depth, cv2.COLORMAP_INFERNO)

    combined_result = cv2.hconcat([img_raw,  depth_color])
            
    cv2.imwrite("output-ax.png", combined_result)
    
    return depth


if __name__ == "__main__":
    args = parse_args()
    infer(**vars(args))
