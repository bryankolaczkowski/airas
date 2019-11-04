#!/usr/local/bin/Rscript

# We need to calculate the distance of each (labelled) ancestral     #
# node from the root node of the tree                                #
#                                                                    #
# We'll use R's "ape" package to do this.                            #
#                                                                    #
# start R, then run thse commands (you could also try to source this #
# file in R, which should do the same thing)                         #
#

library(ape)

for (f in c(Sys.glob("*/brlens_and_labels.tre")))
{
	thedir <- strsplit(f, "/brlens_and_labels.tre")[1]

	thet <- read.tree(file=f)
	root <- length(thet$tip)+1
	total <- length(thet$tip)+length(thet$node)

	ancdists <- dist.nodes(thet)[root,root:total]

	x <- c(thet$node)
	y <- as.vector(ancdists)

	out <- matrix(y,ncol=1,byrow=TRUE)
	rownames(out) <- x
	colnames(out) <- c("dist_from_root")

	outname = paste0(thedir, "/dists_from_root.csv")
	write.csv(out, file=outname, quote=FALSE, eol="\n", row.names=TRUE)
}

quit()
