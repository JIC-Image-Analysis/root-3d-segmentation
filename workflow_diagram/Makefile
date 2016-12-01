workflow.pdf: workflow.gv composite-thumbnail.png wall-thumbnail.png mask-thumbnail.png cells-thumbnail.png watershed-thumbnail.png venus-thumbnail.png intensity_per_cell-thumbnail.png histogram-thumbnail.png
	dot -Tpdf workflow.gv -o workflow.pdf	

composite-thumbnail.png: composite.png
	convert composite.png -resize 256x128 composite-thumbnail.png

wall-thumbnail.png: wall.png
	convert wall.png -resize 256x128 wall-thumbnail.png

venus-thumbnail.png: venus.png
	convert venus.png -resize 256x128 venus-thumbnail.png

mask-thumbnail.png: mask.png
	convert mask.png -resize 256x128 mask-thumbnail.png

watershed-thumbnail.png: watershed.png
	convert watershed.png -resize 256x128 watershed-thumbnail.png

histogram-thumbnail.png: histogram.png
	convert histogram.png -resize 256x256 histogram-thumbnail.png

cells-thumbnail.png: cells.png
	convert cells.png -resize 256x128 cells-thumbnail.png

intensity_per_cell-thumbnail.png: intensity_per_cell.png
	convert intensity_per_cell.png -resize 256x128 intensity_per_cell-thumbnail.png

clean:
	rm workflow.pdf
	rm *-thumbnail.png
