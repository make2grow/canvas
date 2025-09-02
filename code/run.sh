#DIR=simple_examples
#DIR=adv_examples
DIR=canvasapi_examples

if [ ! -d $DIR ]; then
  mkdir $DIR
fi

cd $DIR
uv init .
cp ../requirements.txt .

if [ ! -d "./.venv" ]; then
  uv venv
fi

uv add -r requirements.txt
