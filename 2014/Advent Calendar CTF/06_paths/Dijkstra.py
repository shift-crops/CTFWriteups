#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class ReprMixin(object):
    ''' オブジェクトのアトリビュートを整形して表示するためのミックスインクラス (デバッグ用) '''

    def __repr__(self):
        attr_list = ['%s=%s' % (k, v) for k, v in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attr_list))


class CostCompareMixin(object):
    ''' "cost" アトリビュートを元にオブジェクトの大小を比較するためのミックスインクラス '''

    def __cmp__(self, other):
        return self.cost - other.cost


class Node(ReprMixin,
           CostCompareMixin):
    ''' グラフのノード '''

    def __init__(self, name, edges=None, cost=sys.maxint):
        # ノードの名前
        self.name = name
        # ノードに紐付いたエッジ
        self.edges = edges or []
        # ノードが処理済みかを示すフラグ
        self.done = False
        # ノードに至るまでに必要な最短経路のコスト
        self.cost = cost
        # ノードに至るまでの最短経路を構成する近接したノード
        self.prev_node = None

    def trace(self):
        ''' 自身から逆方向にノードを辿ってリストにする '''
        node = self
        route = [node]
        while node.prev_node:
            route.append(node.prev_node)
            node = node.prev_node
        return route


class Edge(ReprMixin):
    ''' グラフのエッジ '''

    def __init__(self, dst_node, cost):
        # エッジの宛先ノード
        self.dst_node = dst_node
        # エッジのコスト
        self.cost = cost


class DirectedGraph(object):
    ''' 有向グラフ '''

    def __init__(self, mappings):
        self.mappings = mappings

    def shortest_path(self, node_name):
        ''' 開始ノードから指定したノードへの最短経路を取得する '''
        node = self.mappings.get(node_name)
        trace_list = node.trace()
        # 反転させることで最初の要素を開始ノードにする
        trace_list.reverse()
        return trace_list

    @classmethod
    def build(cls, graph_data):
        '''
        有効グラフを構成するデータから有効グラフオブジェクトを生成するためのファクトリメソッド
        グラフデータはシーケンスで、各エントリは 3 要素のタプルから成る
        エントリ: (遷移元ノード名, 遷移先ノード名, 遷移コスト)
        '''
        mappings = {}
        # グラフデータの各エントリを処理する
        for src_node_name, dst_node_name, edge_cost in graph_data:

            # 遷移元ノード、遷移先ノードを取得する
            src_node = cls._get_node(src_node_name, mappings)
            dst_node = cls._get_node(dst_node_name, mappings)

            # ノードをエッジで結ぶ
            edge = Edge(dst_node, edge_cost)
            src_node.edges.append(edge)

        # ノードとエッジから成る有向グラフを返す
        return DirectedGraph(mappings)

    @classmethod
    def _get_node(cls, name, mappings):
        ''' 既知のノードであれば取得、そうでなければ新たに作る '''
        node = mappings.get(name)
        if not node:
            node = Node(name)
            mappings[name] = node
        return node


class Dijkstra(object):
    ''' ダイクストラ法の実装 '''

    @classmethod
    def process(cls, graph, start_node_name):
        ''' ダイクストラ法で開始ノードからの最短経路を探索するメソッド '''

        # 開始ノードの遷移コストを 0 に初期化する
        start_node = graph.mappings.get(start_node_name)
        start_node.cost = 0

        while True:
            # 未処理のノードの中からコストが最小のものを選び出す
            node = cls._extract_unsettled_minimum_node(graph)
            if not node:
                # 未処理のノードが無くなったら抜ける
                break
            # ノードを処理する
            cls._process_node(node)

    @classmethod
    def _extract_unsettled_minimum_node(cls, graph):
        # グラフから未処理のノードを取り出す
        unsettled_nodes = [
            node for node in graph.mappings.values() if not node.done
        ]
        # 最小コストのものを選んで返す
        return min(unsettled_nodes) if unsettled_nodes else None

    @classmethod
    def _process_node(cls, node):
        ''' ノードを処理する '''

        # ノードを処理済みにする
        node.done = True

        # ノードが持つ処理対象のエッジと宛先ノードを取り出す (処理済みのノードは除外する)
        edge_and_nodes = [
            (edge, edge.dst_node) for edge in node.edges
            if not edge.dst_node.done
        ]

        # 処理対象のエッジ、宛先ノードを走査する
        for edge, dst_node in edge_and_nodes:

            # 今処理中のエッジを通って宛先ノードに至るまでのコストと、
            # 宛先ノードに現在設定されているコストを比較する
            current_path_cost = node.cost + edge.cost
            if current_path_cost < dst_node.cost:

                # 処理中のパスの方が短ければ、そちらを使う
                dst_node.cost = current_path_cost

                # 宛先ノードの遷移元ノードを、現在処理中のノードに変更する
                dst_node.prev_node = node


if __name__ == '__main__':
    # グラフを生成する
    graph = DirectedGraph.build([
        ('s', 'a', 2),
        ('s', 'b', 5),
        ('a', 'b', 2),
        ('a', 'c', 5),
        ('b', 'c', 4),
        ('b', 'd', 2),
        ('c', 'z', 7),
        ('d', 'c', 5),
        ('d', 'z', 2),
    ])

    # ノード 's' から各ノードへの最短経路を探索する
    Dijkstra.process(graph, 's')

    # ノード 'z' への最短経路を取り出す
    route = [(node.name, node.cost) for node in graph.shortest_path('z')]

    # 最短経路を表示する
    print('Route: %s' % route)
