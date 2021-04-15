
class Parser:

  ##### Parser header #####
  def __init__(self, scanner):
    self.next_token = scanner.next_token
    self.token = self.next_token()

  def take_token(self, token_type):
    if self.token.type != token_type:
      self.error(f"Error in line {self.token.line} column {self.token.column}. Unexpected type ({self.token.type} != {token_type})")
    if token_type != 'EOF':
      self.token = self.next_token()

  def error(self,msg):
    raise RuntimeError('Parser error, %s' % msg)

  ##### Parser body #####

  # Starting symbol
  def start(self):
    self.take_token('NEWLINE')
    self.version()
    self.program()
    self.take_token('EOF')
    

  def version(self):
    #prod_version -> VERSION COLON SPACE STRING NEWLINE
    if self.token.type =='version':
      print("Checking version...")
      self.take_token('version')
      self.take_token('COLON')
      self.take_token("SPACE")
      self.take_token("STRING")
      self.take_token('NEWLINE')      
      print('VERSION ok')
    # prod_version -> epsilon
    else:
      pass

  def program(self):
    # program -> prod_services program
    if self.token.type == 'services':
      self.services()
      print('SERVICES okk')
      self.program()
    # program -> prod_volume program
    elif self.token.type == 'volumes':
      self.prod_volumes()
      self.program()
    # program -> prod_networks program
    elif self.token.type == 'networks':
      self.prod_networks()
      self.program()
    # program -> NEWLINE program
    elif self.token.type == 'NEWLINE':
      self.take_token('NEWLINE')
      self.program()
    # program -> eps
    else:
      pass

  def services(self):
    #prod_servies -> SERVICES COLON NEWLINE servicesID
    if self.token.type == 'services':
      self.take_token('services')
      self.take_token('COLON')
      self.servicesID()
    else:
      self.error("Epsilon not allowed")

  def servicesID(self):
    #servicesID -> tabulator ID COLON NEWLINE tabulator tabulator attributes_services servicesID
    self.take_token('NEWLINE')
    if self.token.type == 'SPACE':
      self.tabulator()
      service_id = self.token.value
      print(f'Checking service " {service_id} "... ')
      self.take_token('ID')
      self.take_token('COLON')
      self.take_token('NEWLINE')
      self.tabulator()
      self.tabulator()
      self.attributes_services()
      self.servicesID()
    #servicesID -> eps
    else:
      pass

  def attributes_services(self):
    if self.token.type == 'SPACE':
      self.tabulator()
      self.tabulator()
    #attributes_services -> tabulator tabulator prod_image attributes_services
    if self.token.type == 'image':
      self.prod_image()
      self.attributes_services()
    #attributes_services -> tabulator tabulator prod_ports attributes_services 
    elif self.token.type == 'ports':
      self.prod_ports()
      self.attributes_services()
    #attributes_services -> tabulator tabulator prod_volumes attributes_services
    elif self.token.type == 'volumes':
      self.prod_volumes()
      self.attributes_services() 
    #attributes_services -> tabulator tabulator prod_networks attributes_services 
    elif self.token.type == 'networks':
      self.prod_networks()
      self.attributes_services()
    #attributes_services -> tabulator tabulator prod_deploy attributes_services
    elif self.token.type == 'deploy':
      self.prod_deploy()
      self.attributes_services()  
    #attributes_services -> tabulator tabulator prod_buoild attributes_services
    elif self.token.type == 'bulid':
      self.prod_build()
      self.attributes_services()
    #attributes_services -> tabulator tabulator prod_enviroment attributes_services
    elif self.token.type == 'enviroment':
      self.prod_enviroment()
      self.attributes_services()
    #attributes_servioces -> eps
    else:
      pass
         
  def prod_image(self):
    #prod_image -> IMAGE COLON SPACE value NEWLINE
    if self.token.type == 'image':
      self.take_token('image')
      self.take_token('COLON')
      self.take_token('SPACE')
      self.value()
      self.take_token('NEWLINE')
      self.tabulator()
      self.tabulator()
      print('prod_image ok')

  def prod_build(self):
    #prod_build -> BUILD COLON SPACE value NEWLINE
    if self.token.type == 'build':
      self.take_token('build')
      self.take_token('COLON')
      self.take_token('SPACE')
      self.value()
      self.take_token('NEWLINE')
      self.tabulator()
      self.tabulator()
      print('prod_build ok')
  
  def prod_environment(self):
    #prod_environment -> ENVIRONMENT COLON SPACE value NEWLINE
    if self.token.type == 'environment':
      self.take_token('environment')
      self.take_token('COLON')
      self.take_token('SPACE')
      self.value()
      self.take_token('NEWLINE')
      self.tabulator()
      self.tabulator()
      print('prod_nevironment ok')

  def prod_ports(self):
    #prod_ports -> PORTS COLON NEWLINE table
    self.take_token('ports')
    self.take_token('COLON')
    self.take_token('NEWLINE')
    self.tabulator()
    self.table()
    print('prod_ports ok')
  
  def prod_volumes(self):
    self.take_token('volumes')
    self.take_token('COLON')
    self.take_token('NEWLINE')
    self.tabulator()
    #prod_volumes -> VOLUMES COLON NEWLINE tabulator table
    if self.token.type == 'SPACE':
      self.table()
      print('prod_volumes ok')
    #prod_volumes -> VOLUMES COLON NEWLINE tabulator ID COLON NEWLINE  
    elif self.token.type == 'ID':
      self.value()
      #self.take_token('COLON')
      print('VOLUMES ok')
  
  def prod_networks(self):
    self.take_token('networks')
    self.take_token('COLON')
    self.take_token('NEWLINE')
    self.tabulator()
    #prod_networks -> NETWORKS COLON NEWLINE tabulator table
    if self.token.type == 'SPACE':
      self.table()
      print('prod_networks ok')
    #prod_networks -> NETWORKS COLON NEWLINE tabulator ID COLON NEWLINE  
    elif self.token.type == 'ID':
      self.take_token('ID')
      self.take_token('COLON')
      print('NETWORKS ok')

  def prod_deploy(self):
    #prod_deploy -> DEPLOY COLON NEWLINE deploy_atributes
    self.take_token('deploy')
    self.take_token('COLON')
    self.take_token('NEWLINE')
    self.deploy_atributes()
    print('prod_deploy ok')

  def deploy_atributes(self):
    if self.token.type == 'SPACE':
      self.tabulator()
      self.tabulator()
      if self.token.type == 'SPACE':
        self.tabulator()
        # deploy_attributes -> tabulator tabulator MODE COLON SPACE value NEWLINE deploy_attributes
        if self.token.type == 'mode':
          self.take_token('mode')
          self.take_token('COLON')
          self.take_token('SPACE')
          self.value()
          self.take_token('NEWLINE')
          self.deploy_atributes()
        # deploy_attributes -> tabulator tabulator REPLICAS COLON SPACE value NEWLINE deploy_attributes
        elif self.token.type == 'replicas':
          self.take_token('replicas')
          self.take_token('COLON')
          self.take_token('SPACE')
          self.value()
          self.take_token('NEWLINE')
          self.deploy_atributes()
        # deploy_attributes -> tabulator tabulator ENDPOINT_MODE COLON SPACE value NEWLINE deploy_attributes
        elif self.token.type == 'endpoint_mode':
          self.take_token('endpoint_mode')
          self.take_token('COLON')
          self.take_token('SPACE')
          self.value()
          self.take_token('NEWLINE')
          self.deploy_atributes()
      else:
        pass
    else: 
      pass

  def value(self):
    #value -> ID
    if self.token.type == 'ID':
      self.take_token('ID')
      if self.token.type == 'DASH':
        self.take_token('DASH')
        self.take_token('ID')
        self.take_token('COLON')
        if self.token.type == 'PATH':
          self.take_token('PATH')
        else:
          pass
      else:
        pass
    #value -> STRING
    elif self.token.type == 'STRING':
      self.take_token('STRING')
    #value -> NUMBER
    elif self.token.type == 'NUMBER':
      self.take_token('NUMBER')
    #value -> PATH
    elif self.token.type == 'PATH':
      self.take_token('PATH')
    else:
      self.error("Epsilon not allowed")
        
  def table(self):
    #table -> tabulator tabulator DASH SPACE value NEWLINE table
    self.tabulator()
    if self.token.type == 'SPACE':
      self.tabulator()
      self.take_token('DASH')
      self.take_token('SPACE')
      self.value()
      self.take_token('NEWLINE')
      self.tabulator()
      self.table()
    else:
      pass
  
  def tabulator(self):
    #tabulator -> SPACE SPACE
    self.take_token('SPACE')
    self.take_token('SPACE')
