# Data Augmentation Deepfake Audio

## Training Commands

### Experiment 1
python DeepSpeech.py --n_hidden 2048 --checkpoint_dir ../deepspeech-0.9.3-checkpoint --epochs 200 --train_files ../train.csv --dev_files ../dev.csv --test_files ../test.csv --learning_rate 0.0001 --load_cudnn --train_batch_size 32 --dev_batch_size 32 --test_batch_size 32 --export_dir .
python DeepSpeech.py --n_hidden 2048 --checkpoint_dir ../deepspeech-0.9.3-checkpoint --epochs 200 --train_files ../train.csv --dev_files ../dev.csv --test_files ../test.csv --learning_rate 0.0001 --load_cudnn --train_batch_size 32 --dev_batch_size 32 --test_batch_size 32 --dropout_rate 0.40 --export_dir .
python DeepSpeech.py --n_hidden 2048 --checkpoint_dir ../deepspeech-0.9.3-checkpoint --epochs 200 --train_files ../train.csv --dev_files ../dev.csv --test_files ../test.csv --learning_rate 0.0001 --load_cudnn --train_batch_size 32 --dev_batch_size 32 --test_batch_size 32 --scorer_path ../default.scorer --export_dir .


### Experiment 2
python DeepSpeech.py --n_hidden 2048 --checkpoint_dir ../deepspeech-0.9.3-checkpoint --epochs 200 --train_files ../train.csv --dev_files ../dev.csv --test_files ../test.csv --learning_rate 0.0001 --load_cudnn --train_batch_size 32 --dev_batch_size 32 --test_batch_size 32 --export_dir .
python DeepSpeech.py --n_hidden 2048 --checkpoint_dir ../deepspeech-0.9.3-checkpoint --epochs 200 --train_files ../train.csv --dev_files ../dev.csv --test_files ../test.csv --learning_rate 0.0001 --load_cudnn --train_batch_size 32 --dev_batch_size 32 --test_batch_size 32 --dropout_rate 0.40 --export_dir .
python DeepSpeech.py --n_hidden 2048 --checkpoint_dir ../deepspeech-0.9.3-checkpoint --epochs 200 --train_files ../train.csv --dev_files ../dev.csv --test_files ../test.csv --learning_rate 0.0001 --load_cudnn --train_batch_size 32 --dev_batch_size 32 --test_batch_size 32 --scorer_path ../default.scorer --export_dir .
