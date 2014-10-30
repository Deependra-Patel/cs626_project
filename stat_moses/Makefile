FOLDER=../corpus/
DATA_FOLDER = ./data
CUR_FOLDER = .

all: train

train: clean
	@mkdir -p $(DATA_FOLDER)
	@cp $(FOLDER)tuning/tune_sql.txt  $(DATA_FOLDER)
	@cp $(FOLDER)tuning/tune_en.txt  $(DATA_FOLDER)
	@cp $(FOLDER)training/train_en.txt  $(DATA_FOLDER)/train.en
	@cp $(FOLDER)training/train_sql.txt  $(DATA_FOLDER)/train.sql
	@cp $(FOLDER)testing/test_en.txt  $(DATA_FOLDER)
	@cp $(FOLDER)testing/ref_sql.txt  $(DATA_FOLDER)
	@cp $(FOLDER)data.sql  $(DATA_FOLDER)
	@echo "BUILDING LANGUAGE MODEL..."
	@$(CUR_FOLDER)/srilm/bin/i686-m64/ngram-count -order 5 -interpolate -wbdiscount -text $(DATA_FOLDER)/train.sql -lm $(DATA_FOLDER)/sql.lm
	@mkdir -p $(DATA_FOLDER)/train
	@$(CUR_FOLDER)/mosesdecoder-RELEASE-1.0/scripts/training/train-model.perl -root-dir $(DATA_FOLDER)/train -corpus $(DATA_FOLDER)/train -f en -e sql -alignment  grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:5:$(PWD)/$(DATA_FOLDER)/sql.lm:0 --external-bin-dir $(PWD)/$(CUR_FOLDER)/tools/bin/
	#@mkdir -p working
	#@ ../mosesdecoder-RELEASE-1.0/scripts/training/mert-moses.pl tune_sql.txt tune_en.txt ../mosesdecoder-RELEASE-1.0/bin/moses train/model/moses.ini --mertdir ../mosesdecoder-RELEASE-1.0/bin/ &> mert.out
	
test:
	@$(CUR_FOLDER)/mosesdecoder-RELEASE-1.0/bin/moses -f $(DATA_FOLDER)/train/model/moses.ini < $(DATA_FOLDER)/test_en.txt >$(DATA_FOLDER)/output_sql.txt
	@echo "OUTPUT GENERATED IN $(DATA_FOLDER)/output_sql.txt"
clean:
	@echo "CLEANING SYSTEM.."
	@rm -rf $(DATA_FOLDER)

	

