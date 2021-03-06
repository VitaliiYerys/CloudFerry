import unittest

from generate_load import Prerequisites


class ResourceMigrationTests(unittest.TestCase):

    def setUp(self):
        self.src_cloud = Prerequisites(cloud_prefix='SRC')
        self.dst_cloud = Prerequisites(cloud_prefix='DST')

    def validate_resource_parameter_in_dst(self, src_list, dst_list,
                                           resource_name='resource',
                                           parameter='name'):
        # Validating only uniq parameter's value
        self.assertTrue(
            set([x.__dict__[parameter] for x in src_list]).issubset(
                set([x.__dict__[parameter] for x in dst_list])),
            'Not all %ss migrated correctly' % resource_name
        )

    def validate_neutron_resource_parameter_in_dst(self, src_list, dst_list,
                                                   resource_name='networks',
                                                   parameter='name'):
        self.assertTrue(
            set([x[parameter] for x in src_list[resource_name]]).issubset(
                set([x[parameter] for x in dst_list[resource_name]])),
            'Not all %s migrated correctly' % resource_name)

    def test_migrate_keystone_users(self):
        src_users = self.src_cloud.keystoneclient.users.list()
        dst_users = self.dst_cloud.keystoneclient.users.list()

        self.validate_resource_parameter_in_dst(src_users, dst_users,
                                                resource_name='user',
                                                parameter='name')
        self.validate_resource_parameter_in_dst(src_users, dst_users,
                                                resource_name='user',
                                                parameter='email')

    def test_migrate_keystone_roles(self):
        src_roles = self.src_cloud.keystoneclient.roles.list()
        dst_roles = self.dst_cloud.keystoneclient.roles.list()

        self.validate_resource_parameter_in_dst(src_roles, dst_roles,
                                                resource_name='role',
                                                parameter='name')

    def test_migrate_keystone_tenants(self):
        src_tenants = self.src_cloud.keystoneclient.tenants.list()
        dst_tenants = self.dst_cloud.keystoneclient.tenants.list()

        self.validate_resource_parameter_in_dst(src_tenants, dst_tenants,
                                                resource_name='tenant',
                                                parameter='name')
        self.validate_resource_parameter_in_dst(src_tenants, dst_tenants,
                                                resource_name='tenant',
                                                parameter='description')

    def test_migrate_nova_keypairs(self):
        src_keypairs = self.src_cloud.novaclient.keypairs.list()
        dst_keypairs = self.dst_cloud.novaclient.keypairs.list()

        self.validate_resource_parameter_in_dst(src_keypairs, dst_keypairs,
                                                resource_name='keypair',
                                                parameter='name')
        self.validate_resource_parameter_in_dst(src_keypairs, dst_keypairs,
                                                resource_name='keypair',
                                                parameter='fingerprint')

    def test_migrate_nova_flavors(self):
        src_flavors = self.src_cloud.novaclient.flavors.list()
        dst_flavors = self.dst_cloud.novaclient.flavors.list()

        self.validate_resource_parameter_in_dst(src_flavors, dst_flavors,
                                                resource_name='flavor',
                                                parameter='name')
        self.validate_resource_parameter_in_dst(src_flavors, dst_flavors,
                                                resource_name='flavor',
                                                parameter='ram')
        self.validate_resource_parameter_in_dst(src_flavors, dst_flavors,
                                                resource_name='flavor',
                                                parameter='vcpus')
        self.validate_resource_parameter_in_dst(src_flavors, dst_flavors,
                                                resource_name='flavor',
                                                parameter='disk')
        # Id can be changed, but for now in CloudFerry we moving flavor with
        # its id.
        self.validate_resource_parameter_in_dst(src_flavors, dst_flavors,
                                                resource_name='flavor',
                                                parameter='id')

    def test_migrate_nova_security_groups(self):
        src_sec_gr = self.src_cloud.novaclient.security_groups.list()
        dst_sec_gr = self.dst_cloud.novaclient.security_groups.list()

        self.validate_resource_parameter_in_dst(src_sec_gr, dst_sec_gr,
                                                resource_name='security_group',
                                                parameter='name')
        self.validate_resource_parameter_in_dst(src_sec_gr, dst_sec_gr,
                                                resource_name='security_group',
                                                parameter='description')

    def test_migrate_glance_images(self):
        src_images = self.src_cloud.glanceclient.images.list()
        dst_images = self.dst_cloud.glanceclient.images.list()

        self.validate_resource_parameter_in_dst(src_images, dst_images,
                                                resource_name='image',
                                                parameter='name')
        self.validate_resource_parameter_in_dst(src_images, dst_images,
                                                resource_name='image',
                                                parameter='disk_format')
        self.validate_resource_parameter_in_dst(src_images, dst_images,
                                                resource_name='image',
                                                parameter='container_format')
        self.validate_resource_parameter_in_dst(src_images, dst_images,
                                                resource_name='image',
                                                parameter='size')
        self.validate_resource_parameter_in_dst(src_images, dst_images,
                                                resource_name='image',
                                                parameter='checksum')

    def test_migrate_neutron_networks(self):
        src_nets = self.src_cloud.neutronclient.list_networks()
        dst_nets = self.dst_cloud.neutronclient.list_networks()

        self.validate_neutron_resource_parameter_in_dst(src_nets, dst_nets)
        self.validate_neutron_resource_parameter_in_dst(
            src_nets, dst_nets, parameter='provider:network_type')

    def test_migrate_neutron_subnets(self):
        src_subnets = self.src_cloud.neutronclient.list_subnets()
        dst_subnets = self.dst_cloud.neutronclient.list_subnets()

        self.validate_neutron_resource_parameter_in_dst(
            src_subnets, dst_subnets, resource_name='subnets')
        self.validate_neutron_resource_parameter_in_dst(
            src_subnets, dst_subnets, resource_name='subnets',
            parameter='gateway_ip')
        self.validate_neutron_resource_parameter_in_dst(
            src_subnets, dst_subnets, resource_name='subnets',
            parameter='cidr')

    def test_migrate_neutron_routers(self):
        src_routers = self.src_cloud.neutronclient.list_routers()
        dst_routers = self.dst_cloud.neutronclient.list_routers()

        self.validate_neutron_resource_parameter_in_dst(
            src_routers, dst_routers, resource_name='routers')

    def test_migrate_vms_parameters(self):
        src_vms = self.src_cloud.novaclient.servers.list(
            search_opts={'all_tenants': 1})
        dst_vms = self.dst_cloud.novaclient.servers.list(
            search_opts={'all_tenants': 1})

        src_vms = [vm for vm in src_vms if vm.__dict__['status'] != 'ERROR']

        self.validate_resource_parameter_in_dst(
            src_vms, dst_vms, resource_name='VM', parameter='name')
        self.validate_resource_parameter_in_dst(
            src_vms, dst_vms, resource_name='VM', parameter='config_drive')
        self.validate_resource_parameter_in_dst(
            src_vms, dst_vms, resource_name='VM', parameter='key_name')

    def test_migrate_cinder_volumes(self):
        src_volume_list = self.src_cloud.cinderclient.volumes.list(
            search_opts={'all_tenants': 1})
        dst_volume_list = self.dst_cloud.cinderclient.volumes.list(
            search_opts={'all_tenants': 1})

        self.validate_resource_parameter_in_dst(
            src_volume_list, dst_volume_list, resource_name='volume',
            parameter='display_name')
        self.validate_resource_parameter_in_dst(
            src_volume_list, dst_volume_list, resource_name='volume',
            parameter='size')

    @unittest.skip("Temporarily disabled: snapshots doesn't implemented in "
                   "cinder's nfs driver")
    def test_migrate_cinder_snapshots(self):
        src_volume_list = self.src_cloud.cinderclient.volume_snapshots.list(
            search_opts={'all_tenants': 1})
        dst_volume_list = self.dst_cloud.cinderclient.volume_snapshots.list(
            search_opts={'all_tenants': 1})

        self.validate_resource_parameter_in_dst(
            src_volume_list, dst_volume_list, resource_name='volume',
            parameter='display_name')
        self.validate_resource_parameter_in_dst(
            src_volume_list, dst_volume_list, resource_name='volume',
            parameter='size')
