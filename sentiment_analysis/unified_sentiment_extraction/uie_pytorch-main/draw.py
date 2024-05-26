from visual_analysis import *


def default_visual_analysis(args):
    # checking generating environment
    if os.path.exists(args.save_dir):
        shutil.rmtree(args.save_dir)
    os.makedirs(args.save_dir)
    # update sentiment prompt according to task type
    if args.options:
        PROMPT_ITEMS["options"] = args.options
    else:
        if args.task_type == "ext":
            PROMPT_ITEMS["options"] = [
                PROMPT_ITEMS["positive_option"],
                PROMPT_ITEMS["negative_option"],
                PROMPT_ITEMS["not_mentioned_option"],
            ]
        else:
            PROMPT_ITEMS["options"] = [PROMPT_ITEMS["positive_option"], PROMPT_ITEMS["negative_option"]]
    PROMPT_ITEMS["sentiment_prompt"] = PROMPT_ITEMS["sentiment_prompt_prefix"] + "[{}]".format(
        ",".join(PROMPT_ITEMS["options"])
    )

    # define sr to process the result of sentiment analysis
    logger.info("Trying to parse sentiment analysis result: {}".format(args.file_path))
    sr = SentimentResult(args.file_path)
    # define vs to visualize sentiment result
    vs = VisualSentiment(font_path=args.font_path)
    logger.info("Start to generate visual hotel_images of sentiment analysis for you.")
    # visualize aspect with frequency
    if args.task_type == "ext" and sr.aspect_frequency:
        save_path = os.path.join(args.save_dir, "aspect_wc.png")
        vs.plot_aspect_with_frequency(sr.aspect_frequency, save_path, image_type="wordcloud")
        save_path = os.path.join(args.save_dir, "aspect_hist.png")
        vs.plot_aspect_with_frequency(sr.aspect_frequency, save_path, image_type="histogram")
    # visualize opinion with frequency
    if args.task_type == "ext" and sr.opinion_frequency:
        save_path = os.path.join(args.save_dir, "opinion_wc.png")
        vs.plot_opinion_with_frequency(sr.opinion_frequency, save_path, image_type="wordcloud")
        save_path = os.path.join(args.save_dir, "opinion_hist.png")
        vs.plot_opinion_with_frequency(sr.opinion_frequency, save_path, image_type="histogram")
    # visualize aspect and opinion
    if args.task_type == "ext" and sr.aspect_opinion:
        save_path = os.path.join(args.save_dir, "aspect_opinion_wc.png")
        vs.plot_aspect_with_opinion(sr.aspect_opinion, save_path, image_type="wordcloud", sentiment="all")
        save_path = os.path.join(args.save_dir, "aspect_opinion_hist.png")
        vs.plot_aspect_with_opinion(sr.aspect_opinion, save_path, image_type="histogram", sentiment="all", top_n=8)
    # visualize positive aspect and opinion
    if args.task_type == "ext" and sr.aspect_opinion_positives:
        save_path = os.path.join(args.save_dir, "aspect_opinion_wc_pos.png")
        vs.plot_aspect_with_opinion(
            sr.aspect_opinion_positives, save_path, image_type="wordcloud", sentiment="positive"
        )
        save_path = os.path.join(args.save_dir, "aspect_opinion_hist_pos.png")
        vs.plot_aspect_with_opinion(
            sr.aspect_opinion_positives, save_path, image_type="histogram", sentiment="positive", top_n=8
        )
    # visualize negative aspect and opinion
    if args.task_type == "ext" and sr.aspect_opinion_negatives:
        save_path = os.path.join(args.save_dir, "aspect_opinion_wc_neg.png")
        vs.plot_aspect_with_opinion(
            sr.aspect_opinion_negatives, save_path, image_type="wordcloud", sentiment="negative"
        )
        save_path = os.path.join(args.save_dir, "aspect_opinion_hist_neg.png")
        vs.plot_aspect_with_opinion(
            sr.aspect_opinion_negatives, save_path, image_type="histogram", sentiment="negative", top_n=8
        )
    # visualize aspect and sentiment
    if args.task_type == "ext" and sr.aspect_sentiment:
        save_path = os.path.join(args.save_dir, "aspect_sentiment_wc.png")
        vs.plot_aspect_with_sentiment(sr.aspect_sentiment, save_path, image_type="wordcloud")
        save_path = os.path.join(args.save_dir, "aspect_sentiment_hist.png")
        vs.plot_aspect_with_sentiment(
            sr.aspect_sentiment, save_path, image_type="histogram", top_n=15, descend_aspects=sr.descend_aspects
        )
    # visualize sentiment polarity for sentence
    if args.task_type == "cls" and sr.sentence_sentiment:
        save_path = os.path.join(args.save_dir, "sentence_sentiment.png")
        vs.plot_sentence_sentiment(sr.sentence_sentiment, save_path)

    if not os.listdir(args.save_dir):
        logger.info(
            "Nothing generated for task {}, please check that you input the correct parameter task_type or the result of sentiment analysis.".format(
                args.task_type
            )
        )
    else:
        logger.info("Visual hotel_images for sentiment analysis has been saved to: {}".format(args.save_dir))


if __name__ == "__main__":
    # yapf: disable
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", required=True, type=str, help="The result path of sentiment analysis.")
    parser.add_argument("--save_dir", default="./data", type=str, help="The saving path of hotel_images.")
    parser.add_argument("--font_path", default=None, type=str, help="The font Path for showing Chinese in wordcloud.")
    parser.add_argument("--task_type", choices=['ext', 'cls'], default="ext", type=str, help="Two task types [ext, cls] are supported, ext represents the aspect-based extraction task and cls represents the sentence-level classification task, defaults to ext.")
    parser.add_argument("--options", type=str, nargs="+", help="Used only for the classification task, the options for classification")

    args = parser.parse_args()
    # ypdf: enable

    default_visual_analysis(args)
