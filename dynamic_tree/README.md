# Dynamic Tree Algorithm for Hawk
Algorithm to maintain a dynamic tree structure that adapts to the speculation process.

## How to use
- Copy dynamic_tree.py, gen_ea_answer_vicuna.py, gen_ea_alpha_vicuna.py to eagle/evaluation/, and overwrite if needed.
- Copy ea_model.py, cnets.py to eagle/model/ and overwrite the existing files.
- Set the max_position_embeddings to 4096 in the config.json in your base model's directory.
- Set USE_DYNAMIC_TREE to True in gen_ea_answer_vicuna.py and gen_ea_alpha_vicuna.py.
- Run python gen_ea_answer_vicuna.py or gen_ea_alpha_vicuna.py to do the evaluation.
