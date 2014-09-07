extra=
env=vagrant

deploy:
	ansible-playbook -i provisioning/$(env) -e 'env=$(env)' $(extra) provisioning/deploy.yml
