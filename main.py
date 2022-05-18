import transpiler
import tokenizer
import argparse
import logging
import ete3

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parseArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A system for transpiling VladKras -> Mallard-86"
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        action="store",
        default=None,
        help="The file to transpile `--file example.vkl`",
    )

    parser.add_argument(
        "-t",
        "--transpile",
        required=False,
        action="store_true",
        default=True,
        help="Whether or not to transpile the file",
    )

    parser.add_argument(
        "-T",
        "--treeify",
        required=False,
        action="store_true",
        default=False,
        help="Whether or not to create a tree from the dataset",
    )

    parser.add_argument(
        "-i",
        "--image",
        required=False,
        action="store_true",
        default=False,
        help="Whether or not to export a tree image",
    )

    return parser.parse_args()


def checkArguments(args: argparse.Namespace) -> dict:
    if not args.file.endswith(".vkl"):
        raise ValueError("Filename should end with '.vkl'")

    if args.image:
        args.treeify = True

    return {
        "filename": args.file,
        "transpile": args.transpile,
        "image": args.image,
        "treeify": args.treeify,
    }


if __name__ == "__main__":
    args: dict = checkArguments(parseArguments())

    logger.info(f"Analysing: {args['filename']}")

    tokensList: list[tuple] = tokenizer.tokenizeFile(args["filename"])

    logger.info(f"tokenList: {tokensList}")

    if args["treeify"]:
        classedTokensList: list[transpiler.tokenType] = transpiler.treeify(
            tokens=tokensList
        )
        newickTree = transpiler.toNewickTree(
            classedTokensList.currentNode.connectedLowerNodes
        )
        logger.info(f"newickTree: {newickTree}")

    if args["image"]:
        ts: ete3.TreeStyle = ete3.TreeStyle()
        ts.show_leaf_name = True
        ts.scale = 20
        ts.rotation = 90
        newickTree.render("Tree.png", w=1830, units="mm", tree_style=ts)

    if args["transpile"]:
        classTokens = transpiler.cleanInputs(transpiler.tokenify(tokensList))
        classTokens = transpiler.cleanForLoops(classTokens)
        classTokens = transpiler.cleanWhile(classTokens)
        classTokens = transpiler.cleanIfStatement(classTokens)
        transpiledLines = transpiler.transpile(classTokens)
        logger.info(transpiler.numberLines(transpiledLines))
