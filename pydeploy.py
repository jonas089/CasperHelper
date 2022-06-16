import os

# Define a default / backup .sh file to recover on error
_bash_backup = 'casper-client put-deploy --node-address http://136.243.187.84:7777 --chain-name casper-test --secret-key ./key.pem --payment-amount 100000000 --session-path ./counter/target/wasm32-unknown-unknown/release/counter.wasm --session-args'
_bash_name = 'pydeploy.sh'

# Change to argparse later, for now using Inputs
node_address = str(input('Enter Node Address (e.g. http://136.243.187.84:7777): '))
chain_name = input("Enter Chain Name (e.g. casper-test): ")
secret_key = input("Enter Path to Secret key (e.g. ./key.pem): ")
session_path = input("Enter Session WASM path (e.g. ./<CONTRACT_NAME>/target/wasm32-unknown-unknown/release/<CONTRACT_NAME>.wasm): ")
payment_amount = input("Enter Payment Amount (e.g. 1000000000): ")
session_args = ""


# Add as many Session-arguments as you wish and Enter "e" when done ( e stands for exit loop in this context )
while True:
	i = input('Session Arg or Exit (e) if done: ')
	if i == 'e':
		break
	session_args += str(i) + ' '
# Array of tuples to store key and value for easy replacement algorithm to do magic
config = [('--node-address', node_address), ('--chain-name', chain_name), ('--secret-key', secret_key), ('--session-path', session_path), ("--payment-amount", payment_amount), ('--session-args', session_args)]
print('Session Args: ', session_args)
try:
	with open(_bash_name, 'r') as _bash_file:
			_bash = _bash_file.read().split()
# Delete file if exists and create a new one from backup / default
except Exception as CORRUPT:
	print('Bash file corrupt, restoring Bash file.')
	try:
		os.remove(_bash_name)
	except Exception as NO_FILE:
		pass
	open(_bash_name, 'x')
	with open(_bash_name, 'w') as _bash_file:
		_bash_file.write(_bash_backup)
	_bash = _bash_backup.split()

print(_bash)

# Replacement algorithm "updates" the bash file contents
for i in range(0, len(_bash)):
	for e in range(0, len(config)):
		if config[e][0] == _bash[i]:
			try:
				_bash[i+1] = config[e][1]
			except Exception as LIST_ASSIGNMENT_ERROR: #This happens to raise on --session-args, as the default is empty.
				_bash.append(config[e][1])
			continue

# Undo the .split() and write string to the .sh file
print(_bash)
new_bash_str = ''
for key in _bash:
	new_bash_str += key + ' '

print(new_bash_str)

with open(_bash_name, 'w') as _bash_file:
	_bash_file.write(new_bash_str)

# Now the bash file should have been updated. Run ./<NAME_OF_BASH_FILE>.sh to verify.
