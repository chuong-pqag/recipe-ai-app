---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:2407
- loss:CosineSimilarityLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: 'Củ sen bào vỏ 200g.

    Chả cá basa 100g.

    Giò sống 100g.

    Cọng ngò băm 1M.

    Ớt sừng băm 1M.

    Đầu hành lá băm 1M.

    Bột xù 1gói.'
  sentences:
  - Xúc xích chiên xù
  - Củ sen kẹp chả cá basa
  - Viên mè chiên giòn
- source_sentence: 'Nấm đùi gà 150g.

    Lá tàu hủ ky khô 60g (1 lá lớn ).

    Hạt sen 30g.

    Táo đỏ (không hạt) 30g (10 trái ).

    Nấm đông cô (đã luộc) 30g (10 tai nhỏ ).

    Cà rốt 30g.

    Hành tây 30g.

    Tiêu xanh 1nhánh.

    Hành boa rô 20g.

    Bột năng 10g.

    Hạt nêm Aji-ngon® Nấm 8g (2m ).

    Bột ngọt 2g (1/2m).

    Đường 8g (2m).

    Nước tương "Phú Sĩ" 22g (1M).

    Dầu mè 4g (1m).

    RAU NÊM Hành lá tỉa hoa, ngò rí.'
  sentences:
  - Cá đối kho cà chua
  - Canh hến nấu khế
  - Gà hấp tứ quý chay
- source_sentence: 'Cá lóc 1con (500g).

    Củ cải trắng 300g.

    Rau ghém xà lách, rau muống bào, cây chuối bào, cọng súng bào, rau thơm.

    Hành lá, ớt, tiêu, muối, đường.

    Nước mắm, dầu ăn.'
  sentences:
  - Miến xào cua
  - Nghêu nướng mỡ chài
  - Cá lóc kho củ cải
- source_sentence: 'Bí đỏ 100g.

    Cà rốt 100g.

    Đậu bi 100g.

    Cồi sò điệp 200g.

    Ngò rí 2cây.

    Tiêu, bột năng, dầu mè.'
  sentences:
  - Súp cồi điệp rau củ
  - Salad nui
  - Bánh trứng nướng áp chảo
- source_sentence: 'Mực lá làm sạch 250g.

    Hành tây 1/ 2củ.

    Nấm tuyết 1cái.

    Cần tây 150g.

    Sả non bào 1chén.

    Ớt sừng cắt sợi 1trái.

    Gừng non cắt sợi 1M.

    Lá chanh Bắc cắt sợi nhuyễn 1M.

    Tỏi băm, ớt hiểm băm, gừng đập dập.

    Tỏi phi, mè trắng rang, tương ớt.

    Đường, muối, nước mắm.'
  sentences:
  - Bánh cuốn chay
  - Gà hấp hành răm
  - Gỏi mực cay
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision c9745ed1d9f207416be6d2e6f8de32d1f16199bf -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/UKPLab/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 256, 'do_lower_case': False, 'architecture': 'BertModel'})
  (1): Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
  (2): Normalize()
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'Mực lá làm sạch 250g.\nHành tây 1/ 2củ.\nNấm tuyết 1cái.\nCần tây 150g.\nSả non bào 1chén.\nỚt sừng cắt sợi 1trái.\nGừng non cắt sợi 1M.\nLá chanh Bắc cắt sợi nhuyễn 1M.\nTỏi băm, ớt hiểm băm, gừng đập dập.\nTỏi phi, mè trắng rang, tương ớt.\nĐường, muối, nước mắm.',
    'Gỏi mực cay',
    'Gà hấp hành răm',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.9936, 0.9915],
#         [0.9936, 1.0000, 0.9922],
#         [0.9915, 0.9922, 1.0000]])
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 2,407 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                          | sentence_1                                                                       | label                                                         |
  |:--------|:------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:--------------------------------------------------------------|
  | type    | string                                                                              | string                                                                           | float                                                         |
  | details | <ul><li>min: 16 tokens</li><li>mean: 74.23 tokens</li><li>max: 221 tokens</li></ul> | <ul><li>min: 4 tokens</li><li>mean: 9.26 tokens</li><li>max: 21 tokens</li></ul> | <ul><li>min: 1.0</li><li>mean: 1.0</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | sentence_1                              | label            |
  |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------|
  | <code>Cá rô phi 1con (1kg).<br>Hành tím băm 3M.<br>Hạt mắc khén 2m.<br>Húng lủi cắt nhỏ 2M.<br>Húng quế cắt nhỏ 2M.<br>Sả băm 2M.<br>Ớt sừng bỏ hạt, cắt nhỏ 1quả.</code>                                                                                                                                                                                                                                                                                                                                                      | <code>Cá nướng Pa Pỉnh Tộp</code>       | <code>1.0</code> |
  | <code>Ốc lác con vừa 1kg.<br>Thơm 1/ 2trái.<br>Lá chúc 10lá.<br>Sả 5cây.<br>Ớt hiểm 3quả.<br>Tắc 5trái.<br>Ớt sừng cắt sợi.</code>                                                                                                                                                                                                                                                                                                                                                                                             | <code>Ốc xào thơm</code>                | <code>1.0</code> |
  | <code>Thịt thăn bò 300g.<br>Cần tây 50g (1 bẹ ).<br>Ớt chuông đỏ, vàng 100g (50g mỗi loại ).<br>Cà bi 84g (5 trái ).<br>Hành tây tím 47g (1/2 củ ).<br>Cải mầm 3 màu 80g.<br>Chanh vàng 1quả.<br>Nước tương Phú Sĩ giảm muối 27g (1,5M ).<br>Dầu ăn 5g (1M ).<br>Bơ lạt 10g (1,5m).<br>Hạt nêm AjiNgon Heo 2g (1/2m).<br>Đường 6g (1/2 M).<br>Giấm 10g (2M).<br>Tiêu 1/ 3m.<br>AjiQuick bột tẩm khô chiên giòn 21g (Nửa gói).<br>Mè rang 2m.<br>Tỏi băm 1/ 2M.<br>Ăn trưa kèm Cơm, Ốc xào khế, Canh chua bông thiên lý.</code> | <code>Thịt bò chiên trộn cải mầm</code> | <code>1.0</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `overwrite_output_dir`: False
- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `per_gpu_train_batch_size`: None
- `per_gpu_eval_batch_size`: None
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 3
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: {}
- `warmup_ratio`: 0.0
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `save_safetensors`: True
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `no_cuda`: False
- `use_cpu`: False
- `use_mps_device`: False
- `seed`: 42
- `data_seed`: None
- `jit_mode_eval`: False
- `use_ipex`: False
- `bf16`: False
- `fp16`: False
- `fp16_opt_level`: O1
- `half_precision_backend`: auto
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: 0
- `ddp_backend`: None
- `tpu_num_cores`: None
- `tpu_metrics_debug`: False
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `past_index`: -1
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_min_num_params`: 0
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `fsdp_transformer_layer_cls_to_wrap`: None
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `adafactor`: False
- `group_by_length`: False
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `use_legacy_prediction_loop`: False
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_inputs_for_metrics`: False
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `fp16_backend`: auto
- `push_to_hub_model_id`: None
- `push_to_hub_organization`: None
- `mp_parameters`: 
- `auto_find_batch_size`: False
- `full_determinism`: False
- `torchdynamo`: None
- `ray_scope`: last
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_tokens_per_second`: False
- `include_num_input_tokens_seen`: False
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Framework Versions
- Python: 3.12.8
- Sentence Transformers: 5.1.0
- Transformers: 4.56.0
- PyTorch: 2.8.0+cpu
- Accelerate: 1.10.1
- Datasets: 4.0.0
- Tokenizers: 0.22.0

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->