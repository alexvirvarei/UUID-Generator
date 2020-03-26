import unittest
import time

import Node

class TestNode(unittest.TestCase):
    # brute-forcing the node to ensure sequence uniqueness
    def testBruteForce(self):
        test_node = Node.Node(44)
        last_uuid = -1
        
        for i in range(1000000):
            uuid = test_node.get_id()
            self.assertNotEqual(last_uuid,uuid)
            last_uuid = uuid


    # testing 100.000 requests in 1 second to ensure uniqueness and performance
    def testSequence(self):
        test_node = Node.Node(73)
        last_uuid = -1
        
        t_start = time.perf_counter()
        
        for i in range(100000):
            uuid = test_node.get_id()
            self.assertNotEqual(last_uuid,uuid)
            last_uuid = uuid

        t_stop = time.perf_counter()
        # ensuring performance
        self.assertLess(t_stop - t_start, 1)

    # testing uniqueness after node crash:
    def testPostCrash(self):
        # first testing the case where the node barely got to generate 100 uids,
        # which happens really fast
        test_node = Node.Node(111)
        pre_crash = [test_node.get_id() for i in range(100)]
        del test_node
        test_node = Node.Node(111)
        post_crash = [test_node.get_id() for i in range(100)]

        s = set(pre_crash)
        difference = len([x for x in post_crash if x not in s])
        
        self.assertEqual(difference,100)
        del test_node

        # now testing the case where the node got to generate 100.000 uids
        test_node = Node.Node(111)
        pre_crash = [test_node.get_id() for i in range(100000)]
        del test_node
        test_node = Node.Node(111)
        post_crash = [test_node.get_id() for i in range(100000)]

        s = set(pre_crash)
        difference = len([x for x in post_crash if x not in s])
        
        self.assertEqual(difference,100000)

    # brute-forcing 2 node with different IDs in the same time to ensure uniqueness
    def testIDUniqueness(self):
        test_node1 = Node.Node(451)
        test_node2 = Node.Node(452)


        for i in range(1000000):
            uuid1 = test_node1.get_id()
            uuid2 = test_node2.get_id()
            self.assertNotEqual(uuid1,uuid2)
            

        node1_uuids = []
        node2_uuids = []

        for i in range(100000):
            node1_uuids.append(test_node1.get_id())
            node2_uuids.append(test_node2.get_id())

        s = set(node1_uuids)
        difference = len([x for x in node2_uuids if x not in s])
        
        self.assertEqual(difference,100000)

    # checking all range of IDs for uniqueness (0 - 1023)
    def testIDUniqueness2(self):
        test_nodes = []
        
        for _id in range(1024):
            test_nodes.append(Node.Node(_id))

        uuids = []
        for node in test_nodes:
            for i in range(10):
                uuids.append(node.get_id())

        self.assertEqual(len(uuids),len(set(uuids)))

def main():
    unittest.main()

if __name__ == "__main__":
    main()

