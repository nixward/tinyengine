# ----------------------------------------------------------------------
# Project: TinyEngine
# Title:   maxpool2d.py
#
# Reference papers:
#  - MCUNet: Tiny Deep Learning on IoT Device, NeurIPS 2020
#  - MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning, NeurIPS 2021
#  - MCUNetV3: On-Device Training Under 256KB Memory, arXiv:2206.15472
# Contact authors:
#  - Wei-Ming Chen, wmchen@mit.edu
#  - Wei-Chen Wang, wweichen@mit.edu
#  - Ji Lin, jilin@mit.edu
#  - Ligeng Zhu, ligeng@mit.edu
#  - Song Han, songhan@mit.edu
#
# Target ISA:  ARMv7E-M
# ----------------------------------------------------------------------

import warnings

from .basic_utils import basicOperator, deep_copy_dicts, overwrite_dicts

__all__ = ["maxPool2d"]

default_params = {
    # op related
    "op": "MAX_POOL_2D",
    "is_SEBlock": False,
    "filter_h": None,
    "filter_w": None,
    "stride_h": None,
    "stride_w": None,
    "pad_h": None,
    "pad_w": None,
    "input_idx": None,
    "output_idx": None,
    # tensor related
    "input_dim": None,
    "input_h": None,
    "input_w": None,
    "input_c": None,
    "output_dim": None,
    "output_h": None,
    "output_w": None,
    "output_c": None,
    "input_dtype": "int8",
    "output_dtype": "int8",
    # quantization related
    "input_zero_point": None,
    "output_zero_point": None,
    "input_scale": None,
    "output_scale": None,
}


class maxPool2d(basicOperator):
    def __init__(self, params: dict) -> None:
        self.params = deep_copy_dicts(default_params)
        overwrite_dicts(self.params, params)
        super().__init__()
        # handle input/output tensors in HWC format
        self._add_input(
            self.params["input_idx"],
            self.params["input_dtype"],
            self.params["input_c"],
            self.params["input_w"],
            self.params["input_h"],
        )
        self._add_output(
            self.params["output_idx"],
            self.params["output_dtype"],
            self.params["output_c"],
            self.params["output_w"],
            self.params["output_h"],
        )

        if None in default_params:
            warnings.warn(f"parameters are not all set for op {self.params['op']}")

    def generate_inference_str(self):
        params = self.params
        string = f"max_pooling({self._getBufferstr(params['input_buf_add'], params['input_buf_add_offset'])},"
        string += (
            f"{str(params['input_h'])},{str(params['input_w'])},{str(params['input_c'])},{str(params['stride_h'])},"
        )
        string += f"{str(params['stride_w'])},{str(params['output_h'])},{str(params['output_w'])},-128,127,"
        string += f"{self._getBufferstr(params['output_buf_add'], params['output_buf_add_offset'])});\n"

        return string
