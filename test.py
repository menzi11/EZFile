
k=ezfile("C:/Users/mk/source/repos_build/TBTMegaProject_build/Soloist2/detector")
files = k.find_child_files(True,'exe')
print(files)

b=ezfile("C:/Users/mk/source/repos_build/TBTMegaProject_build/Soloist2/detector2")
k.copy_to(b)
b.rename('abc')