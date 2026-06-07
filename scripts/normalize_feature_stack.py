from ij import IJ
from ij import ImageStack
from ij import ImagePlus
from ij.plugin import Duplicator
from ij.measure import Measurements



def main():
    image = IJ.getImage()
    normalizedImage, _ = zScoreNormalizeFeatureStack(image)
    normalizedImage.show()
    
    
    
def zScoreNormalizeFeatureStack(imp):
    stack = imp.getStack()
    nrOfFeatures = stack.getSize()
    normStack = ImageStack()
    for i in range(1, nrOfFeatures+1):
        impSlice = stack.getProcessor(i).duplicate()
        stats = impSlice.getStats()
        floatImageProcessor = impSlice.convertToFloat()
        floatImageProcessor.subtract(stats.umean)
        floatImageProcessor.multiply(1.0 / stats.stdDev)
        normStack.addSlice("f" + str(i), floatImageProcessor)
    normImp = ImagePlus("normalized features of " + imp.getTitle(), normStack)
    IJ.resetMinAndMax(normImp)
    return normImp, nrOfFeatures;   
        
    
    
def normalizeFeatureStack(imp):
    stack = imp.getStack()
    nrOfFeatures = stack.getSize()
    normStack = ImageStack()
    for i in range(1, nrOfFeatures+1):
        impSlice = Duplicator().run(imp, i, i, 1, 1, 1, 1)
        impSlice.show()
        IJ.run("32-bit")
        IJ.run("Divide...", "value=65535 stack")
        normStack.addSlice("f" + str(i), impSlice.getProcessor())
        impSlice.changes = False
        impSlice.close()      
    normImp = ImagePlus("normalized features", normStack)
    IJ.resetMinAndMax(normImp)
    return normImp, nrOfFeatures;
    
    
   
main()