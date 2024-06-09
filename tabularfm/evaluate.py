import os
import argparse
import shutil
from utils import get_config, create_model_config, create_model, get_finetune_paths
from pipelines.evaluation import proceed_scoring

def evaluate(model_type, data_path, finetune_path, fromscratch_path, save_path, config_path, resume):
    
    configs = get_config(config_path)
    model_config_finetune = create_model_config(data_path, configs, model_type, config_type = "finetune")
    model_config_fromscratch = create_model_config(data_path, configs, model_type, config_type = "fromscratch")
    list_data_paths = get_finetune_paths(configs)
    
    if configs['split_set'] is not None:
        score_save_path = os.path.join(save_path, f"score_{configs['split_set']}.csv")
    else:
        # TODO
        pass
    
    proceed_scoring(list_data_paths, configs, model_config_finetune, model_config_fromscratch, model_type, data_path, finetune_path, fromscratch_path, score_save_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, default="stvae", dest="model", help="Path to the training data")
    parser.add_argument("-ft", "--finetune", type=str, dest="finetune_path", help="Path to directory of finetuning")
    parser.add_argument("-fs", "--fromscratch", type=str, dest="fromscratch_path", help="Path to directory of training from scratch")
    parser.add_argument("-d", "--data", type=str, dest="data_path", help="Path to the directory of datasets")
    parser.add_argument("-s", "--save", type=str, dest="save_path", help="Save directory")
    parser.add_argument("-c", "--config", type=str, dest="config", help="Path to the configuration file")
    parser.add_argument('--resume', action=argparse.BooleanOptionalAction, dest="resume", help="Whether to resume training or not")

    args = parser.parse_args()
    
    # if already exist but not resume, then replace
    if os.path.exists(args.save_path) and not args.resume:
        shutil.rmtree(args.save_path)
    
    
    # create save directory if not create
    if not os.path.exists(args.save_path) and not args.resume:
        os.mkdir(args.save_path)
        
    # pretrain
    evaluate(args.model, args.data_path, args.finetune_path, args.fromscratch_path, args.save_path, args.config, args.resume)