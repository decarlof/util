import os, json;

f = open("/local/data/2019-02/Zenyuk/AvCarb/rotation_axis.json");
centers = json.loads(f.read())
f.close()
for key1 in centers:
	for key2, value2 in centers[key1].items():
#		if not os.path.exists("/local/data/2019-02/Zenyuk/slice_rec/recon_"+key2[:-3]+"_00000.tiff"):
		os.system("python rec.py --axis "+"{:.2f}".format(value2)+" /local/data/2019-02/Zenyuk/AvCarb/"+key2)