# main.py
import argparse
import os
import time
from Uutils import load_txt, write_json_file
from paddlenlp import Taskflow
from paddlenlp.utils.log import logger

def run_analysis(file_path, save_path, model="uie-senta-base", load_from_dir=None, schema=None, aspects=None, batch_size=4, max_seq_len=512):
    """
    Predict based on Taskflow.
    """
    start_time = time.time()
    # read file
    logger.info("Trying to load dataset: {}".format(file_path))
    if not os.path.exists(file_path):
        raise ValueError("something with wrong for your file_path, it may not exist.")
    examples = load_txt(file_path)

    # define Taskflow for sentiment analysis
    schema = eval(schema) if schema else [{'评价维度': ['观点词', '情感倾向[正向,负向,未提及]']}]
    if load_from_dir:
        senta = Taskflow(
            "sentiment_analysis",
            model=model,
            schema=schema,
            aspects=aspects,
            batch_size=batch_size,
            max_seq_len=max_seq_len,
            task_path=load_from_dir,
        )
    else:
        senta = Taskflow(
            "sentiment_analysis",
            model=model,
            schema=schema,
            aspects=aspects,
            batch_size=batch_size,
            max_seq_len=max_seq_len,
        )

    # predict with Taskflow
    logger.info("Start to perform sentiment analysis for your dataset, this may take some time.")
    results = senta(examples)

    # save results
    if not save_path:
        save_dir = os.path.dirname(file_path)
        save_path = os.path.join(save_dir, "sentiment_results.json")
    write_json_file(results, save_path)
    logger.info("The results of sentiment analysis has been saved to: {}".format(save_path))
    logger.info("This run take {} seconds.".format(time.time() - start_time))




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file_path", type=str, default=r"D:\develop\pylearn\商品识别评论分析\PaddleNLP-develop\applications\sentiment_analysis\unified_sentiment_extraction\data\shopping.txt", help="The file path that you want to perform sentiment analysis on.")
    parser.add_argument("--save_path", type=str, default=r"D:\develop\pylearn\商品识别评论分析\PaddleNLP-develop\applications\sentiment_analysis\unified_sentiment_extraction\data", help="The saving path for the results of sentiment analysis.")
    parser.add_argument("--model", choices=['uie-senta-base', 'uie-senta-medium', 'uie-senta-mini', 'uie-senta-micro', 'uie-senta-nano'], default="uie-senta-nano", help="The model name that you wanna use for sentiment analysis.")
    parser.add_argument("--load_from_dir", default=None, type=str, help="The directory path for the finetuned model to predict, if set None, it will download model according to model_name.")
    parser.add_argument("--schema", default="[{'评价维度': ['观点词', '情感倾向[正向,负向,未提及]']}]", type=str, help="The schema for UIE to extract infomation.")
    parser.add_argument("--aspects", default=None, type=str, nargs="+", help="A list of pre-given aspects, that is to say, Pipeline only perform sentiment analysis on these pre-given aspects if you input it.")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size per GPU/CPU for training.")
    parser.add_argument("--max_seq_len", type=int, default=512, help="The maximum total input sequence length after tokenization.")

    args = parser.parse_args()
    run_analysis(args.file_path, args.save_path, args.model, args.load_from_dir, args.schema, args.aspects, args.batch_size, args.max_seq_len)



