

__author__ = 'def'


class SimpleMagnetToolhead:
    def __init__(self, *args):
        self.comm = None
        self.type = 'SimpleMagnet'
        self.magnets = []

        for arg in args:
            self.add_magnet(arg)

    def add_magnet(self, pin):
        if pin not in [ magnet['pin'] for magnet in self.magnets]:
            self.magnets.append({'pin':pin, 'status':'off'})

    def set_magnet(self, id, status):
        try:
            # Get value equivalent to the selected status
            if status == 'on':
                value = 255
            elif status == 'off':
                value = 0
            else:
                raise AttributeError('Status %s not supported for magnet %d' % (status, id))

            # Get corresponding pin
            pin = self.magnets[id]['pin']

            # Send command
            self.comm.send('M42 P%d S%d\n' % (pin, value))

            # Change internal status
            self.magnets[id]['status'] = status

        except IndexError:
            raise Exception('Error: magnet %d is not attached to toolhead yet.' % id)
        except AttributeError:
            raise Exception('Error: Toolhead not attached to CoreXY yet.')



    def _set_comm_interface(self, interface):
        self.comm = interface



if __name__ == '__main__':
    from CoreXY import CoreXY
    import time

    # CoreXY startup
    cxy = CoreXY()
    cxy.reset()
    cxy.connect()
    time.sleep(2)

    # Add toolhead
    tool = SimpleMagnetToolhead(4, 5)
    cxy.set_toolhead(tool)
    if len(cxy.toolhead.magnets) == 2:
        if cxy.toolhead.magnets[0]['pin'] != 4 or cxy.toolhead.magnets[0]['status'] != 'off':
            print '[Error] Toolhead configuration of magnet 0 went wrong'
        if cxy.toolhead.magnets[1]['pin'] != 5 or cxy.toolhead.magnets[1]['status'] != 'off':
            print '[Error] Toolhead configuration of magnet 0 went wrong'
    else:
        print '[Error] Tooldhead configuration went wrong: incorrect number of magnets'



    # Use toolhead
    cxy.home()
    cxy.toolhead.set_magnet(0, 'on')

    if cxy.toolhead.magnets[0]['status'] == 'on':
        print '[ok] Magnet turned on!'
    else:
        print '[Error] Could not turn on magnet'

    time.sleep(5)
    cxy.toolhead.set_magnet(0, 'off')

    if cxy.toolhead.magnets[0]['status'] == 'off':
        print '[ok] Magnet turned off!'
    else:
        print '[Error] Could not turn off magnet'

    # Cleanup
    cxy.disconnect()
