SERVER_PORT=8010
MONGO_CONNECTION_STRING=mongodb://boticot:botw0rd@localhost:27017/boticotdb?authSource=admin
MODELS_PATH=./models/
MODEL_LOADER=mongodb
ACTIVATE_LOADER_CRON=1
LOADER_CRON_SCHEDULE=1
CHECK_EXACT_TEXT=1
MAX_PAGE_SIZE=200
JWT_SECRET_KEY=your_boticot_jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRES=240
ADMIN_LOGIN=admin@boticot.ai
ADMIN_PWD=B0tic0t!
TF_XLA_FLAGS=--tf_xla_cpu_global_jit