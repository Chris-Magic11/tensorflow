# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Benchmarks for `tf.data.Dataset.batch()`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from tensorflow.python.data.benchmarks import benchmark_base
from tensorflow.python.data.ops import dataset_ops
from tensorflow.python.framework import sparse_tensor


class BatchBenchmark(benchmark_base.DatasetBenchmarkBase):
  """Benchmarks for `tf.data.Dataset.batch()`."""

  def benchmark_batch_sparse(self):
    non_zeros_per_row_values = [0, 1, 5, 10, 100]
    batch_size_values = [1, 32, 64, 128, 1024]

    for non_zeros_per_row in non_zeros_per_row_values:

      tensor = sparse_tensor.SparseTensor(
          indices=np.arange(non_zeros_per_row, dtype=np.int64)[:, np.newaxis],
          values=np.arange(non_zeros_per_row, dtype=np.int64),
          dense_shape=[1000])

      for batch_size in batch_size_values:
        dataset = dataset_ops.Dataset.from_tensors(tensor).repeat().batch(
            batch_size)
        self.run_and_report_benchmark(
            dataset,
            num_elements=100000 // batch_size,
            iters=1,
            name="sparse_num_elements_%d_batch_size_%d" % (non_zeros_per_row,
                                                           batch_size))


if __name__ == "__main__":
  benchmark_base.test.main()
