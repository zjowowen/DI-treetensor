import pytest
import torch

import treetensor.torch as ttorch


# noinspection DuplicatedCode,PyUnresolvedReferences
@pytest.mark.unittest
class TestTorchFuncs:
    def test_tensor(self):
        t1 = ttorch.tensor(True)
        assert isinstance(t1, torch.Tensor)
        assert t1

        t2 = ttorch.tensor([[1, 2, 3], [4, 5, 6]])
        assert isinstance(t2, torch.Tensor)
        assert (t2 == torch.tensor([[1, 2, 3], [4, 5, 6]])).all()

        t3 = ttorch.tensor({
            'a': [1, 2],
            'b': [[3, 4], [5, 6.2]],
            'x': {
                'c': True,
                'd': [False, True],
            }
        })
        assert isinstance(t3, ttorch.Tensor)
        assert (t3 == ttorch.Tensor({
            'a': torch.tensor([1, 2]),
            'b': torch.tensor([[3, 4], [5, 6.2]]),
            'x': {
                'c': torch.tensor(True),
                'd': torch.tensor([False, True]),
            }
        })).all()

    def test_zeros(self):
        assert ttorch.all(ttorch.zeros(2, 3) == torch.zeros(2, 3))
        assert ttorch.all(ttorch.zeros({
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        }) == ttorch.Tensor({
            'a': torch.zeros(2, 3),
            'b': torch.zeros(5, 6),
            'x': {
                'c': torch.zeros(2, 3, 4),
            }
        }))

    def test_zeros_like(self):
        assert ttorch.all(
            ttorch.zeros_like(torch.tensor([[1, 2, 3], [4, 5, 6]])) ==
            torch.tensor([[0, 0, 0], [0, 0, 0]]),
        )
        assert ttorch.all(
            ttorch.zeros_like({
                'a': torch.tensor([[1, 2, 3], [4, 5, 6]]),
                'b': torch.tensor([1, 2, 3, 4]),
                'x': {
                    'c': torch.tensor([5, 6, 7]),
                    'd': torch.tensor([[[8, 9]]]),
                }
            }) == ttorch.Tensor({
                'a': torch.tensor([[0, 0, 0], [0, 0, 0]]),
                'b': torch.tensor([0, 0, 0, 0]),
                'x': {
                    'c': torch.tensor([0, 0, 0]),
                    'd': torch.tensor([[[0, 0]]]),
                }
            })
        )

    def test_ones(self):
        assert ttorch.all(ttorch.ones(2, 3) == torch.ones(2, 3))
        assert ttorch.all(ttorch.ones({
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        }) == ttorch.Tensor({
            'a': torch.ones(2, 3),
            'b': torch.ones(5, 6),
            'x': {
                'c': torch.ones(2, 3, 4),
            }
        }))

    def test_ones_like(self):
        assert ttorch.all(
            ttorch.ones_like(torch.tensor([[1, 2, 3], [4, 5, 6]])) ==
            torch.tensor([[1, 1, 1], [1, 1, 1]])
        )
        assert ttorch.all(
            ttorch.ones_like({
                'a': torch.tensor([[1, 2, 3], [4, 5, 6]]),
                'b': torch.tensor([1, 2, 3, 4]),
                'x': {
                    'c': torch.tensor([5, 6, 7]),
                    'd': torch.tensor([[[8, 9]]]),
                }
            }) == ttorch.Tensor({
                'a': torch.tensor([[1, 1, 1], [1, 1, 1]]),
                'b': torch.tensor([1, 1, 1, 1]),
                'x': {
                    'c': torch.tensor([1, 1, 1]),
                    'd': torch.tensor([[[1, 1]]]),
                }
            })
        )

    def test_randn(self):
        _target = ttorch.randn(200, 300)
        assert -0.02 <= _target.view(60000).mean().tolist() <= 0.02
        assert 0.98 <= _target.view(60000).std().tolist() <= 1.02
        assert _target.shape == torch.Size([200, 300])

        _target = ttorch.randn({
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        })
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([5, 6]),
            'x': {
                'c': torch.Size([2, 3, 4]),
            }
        })

    def test_randn_like(self):
        _target = ttorch.randn_like(torch.ones(200, 300))
        assert -0.02 <= _target.view(60000).mean().tolist() <= 0.02
        assert 0.98 <= _target.view(60000).std().tolist() <= 1.02
        assert _target.shape == torch.Size([200, 300])

        _target = ttorch.randn_like({
            'a': torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32),
            'b': torch.tensor([1, 2, 3, 4], dtype=torch.float32),
            'x': {
                'c': torch.tensor([5, 6, 7], dtype=torch.float32),
                'd': torch.tensor([[[8, 9]]], dtype=torch.float32),
            }
        })
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([4]),
            'x': {
                'c': torch.Size([3]),
                'd': torch.Size([1, 1, 2]),
            }
        })

    def test_randint(self):
        _target = ttorch.randint(-10, 10, {
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        })
        assert ttorch.all(_target < 10)
        assert ttorch.all(-10 <= _target)
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([5, 6]),
            'x': {
                'c': torch.Size([2, 3, 4]),
            }
        })

        _target = ttorch.randint(10, {
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        })
        assert ttorch.all(_target < 10)
        assert ttorch.all(0 <= _target)
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([5, 6]),
            'x': {
                'c': torch.Size([2, 3, 4]),
            }
        })

    def test_randint_like(self):
        _target = ttorch.randint_like({
            'a': torch.tensor([[1, 2, 3], [4, 5, 6]]),
            'b': torch.tensor([1, 2, 3, 4]),
            'x': {
                'c': torch.tensor([5, 6, 7]),
                'd': torch.tensor([[[8, 9]]]),
            }
        }, -10, 10)
        assert ttorch.all(_target < 10)
        assert ttorch.all(-10 <= _target)
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([4]),
            'x': {
                'c': torch.Size([3]),
                'd': torch.Size([1, 1, 2]),
            }
        })

        _target = ttorch.randint_like({
            'a': torch.tensor([[1, 2, 3], [4, 5, 6]]),
            'b': torch.tensor([1, 2, 3, 4]),
            'x': {
                'c': torch.tensor([5, 6, 7]),
                'd': torch.tensor([[[8, 9]]]),
            }
        }, 10)
        assert ttorch.all(_target < 10)
        assert ttorch.all(0 <= _target)
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([4]),
            'x': {
                'c': torch.Size([3]),
                'd': torch.Size([1, 1, 2]),
            }
        })

    def test_full(self):
        _target = ttorch.full({
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        }, 233)
        assert ttorch.all(_target == 233)
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([5, 6]),
            'x': {
                'c': torch.Size([2, 3, 4]),
            }
        })

    def test_full_like(self):
        _target = ttorch.full_like({
            'a': torch.tensor([[1, 2, 3], [4, 5, 6]]),
            'b': torch.tensor([1, 2, 3, 4]),
            'x': {
                'c': torch.tensor([5, 6, 7]),
                'd': torch.tensor([[[8, 9]]]),
            }
        }, 233)
        assert ttorch.all(_target == 233)
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([4]),
            'x': {
                'c': torch.Size([3]),
                'd': torch.Size([1, 1, 2]),
            }
        })

    def test_empty(self):
        _target = ttorch.empty({
            'a': (2, 3),
            'b': (5, 6),
            'x': {
                'c': (2, 3, 4),
            }
        })
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([5, 6]),
            'x': {
                'c': torch.Size([2, 3, 4]),
            }
        })

    def test_empty_like(self):
        _target = ttorch.empty_like({
            'a': torch.tensor([[1, 2, 3], [4, 5, 6]]),
            'b': torch.tensor([1, 2, 3, 4]),
            'x': {
                'c': torch.tensor([5, 6, 7]),
                'd': torch.tensor([[[8, 9]]]),
            }
        })
        assert _target.shape == ttorch.Size({
            'a': torch.Size([2, 3]),
            'b': torch.Size([4]),
            'x': {
                'c': torch.Size([3]),
                'd': torch.Size([1, 1, 2]),
            }
        })

    def test_all(self):
        r1 = ttorch.all(torch.tensor([True, True, True]))
        assert torch.is_tensor(r1)
        assert r1 == torch.tensor(True)
        assert r1

        r2 = ttorch.all(torch.tensor([True, True, False]))
        assert torch.is_tensor(r2)
        assert r2 == torch.tensor(False)
        assert not r2

        r3 = ttorch.all(torch.tensor([False, False, False]))
        assert torch.is_tensor(r3)
        assert r3 == torch.tensor(False)
        assert not r3

        r4 = ttorch.all({
            'a': torch.tensor([True, True, True]),
            'b': torch.tensor([True, True, True]),
        }).all()
        assert torch.is_tensor(r4)
        assert r4 == torch.tensor(True)
        assert r4

        r5 = ttorch.all({
            'a': torch.tensor([True, True, True]),
            'b': torch.tensor([True, True, False]),
        }).all()
        assert torch.is_tensor(r5)
        assert r5 == torch.tensor(False)
        assert not r5

        r6 = ttorch.all({
            'a': torch.tensor([False, False, False]),
            'b': torch.tensor([False, False, False]),
        }).all()
        assert torch.is_tensor(r6)
        assert r6 == torch.tensor(False)
        assert not r6

    def test_any(self):
        r1 = ttorch.any(torch.tensor([True, True, True]))
        assert torch.is_tensor(r1)
        assert r1 == torch.tensor(True)
        assert r1

        r2 = ttorch.any(torch.tensor([True, True, False]))
        assert torch.is_tensor(r2)
        assert r2 == torch.tensor(True)
        assert r2

        r3 = ttorch.any(torch.tensor([False, False, False]))
        assert torch.is_tensor(r3)
        assert r3 == torch.tensor(False)
        assert not r3

        r4 = ttorch.any({
            'a': torch.tensor([True, True, True]),
            'b': torch.tensor([True, True, True]),
        }).all()
        assert torch.is_tensor(r4)
        assert r4 == torch.tensor(True)
        assert r4

        r5 = ttorch.any({
            'a': torch.tensor([True, True, True]),
            'b': torch.tensor([True, True, False]),
        }).all()
        assert torch.is_tensor(r5)
        assert r5 == torch.tensor(True)
        assert r5

        r6 = ttorch.any({
            'a': torch.tensor([False, False, False]),
            'b': torch.tensor([False, False, False]),
        }).all()
        assert torch.is_tensor(r6)
        assert r6 == torch.tensor(False)
        assert not r6

    def test_eq(self):
        assert ttorch.eq(torch.tensor([1, 2, 3]), torch.tensor([1, 2, 3])).all()
        assert not ttorch.eq(torch.tensor([1, 2, 3]), torch.tensor([1, 2, 2])).all()
        assert ttorch.eq(torch.tensor([1, 1, 1]), 1).all()
        assert not ttorch.eq(torch.tensor([1, 1, 2]), 1).all()

        assert ttorch.eq({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 6]),
        }, ({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 6]),
        })).all()
        assert not ttorch.eq({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 6]),
        }, ({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 5]),
        })).all()

    def test_ne(self):
        assert (ttorch.ne(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[1, 1], [4, 4]]),
        ) == torch.tensor([[False, True],
                           [True, False]])).all()

        assert (ttorch.ne(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': [1.0, 1.5, 2.0],
            }),
            ttorch.tensor({
                'a': [[1, 1], [4, 4]],
                'b': [1.3, 1.2, 2.0],
            }),
        ) == ttorch.tensor({
            'a': [[False, True], [True, False]],
            'b': [True, True, False],
        })).all()

    def test_lt(self):
        assert (ttorch.lt(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[1, 1], [4, 4]]),
        ) == torch.tensor([[False, False],
                           [True, False]])).all()

        assert (ttorch.lt(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': [1.0, 1.5, 2.0],
            }),
            ttorch.tensor({
                'a': [[1, 1], [4, 4]],
                'b': [1.3, 1.2, 2.0],
            }),
        ) == ttorch.tensor({
            'a': [[False, False], [True, False]],
            'b': [True, False, False],
        })).all()

    def test_le(self):
        assert (ttorch.le(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[1, 1], [4, 4]]),
        ) == torch.tensor([[True, False],
                           [True, True]])).all()

        assert (ttorch.le(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': [1.0, 1.5, 2.0],
            }),
            ttorch.tensor({
                'a': [[1, 1], [4, 4]],
                'b': [1.3, 1.2, 2.0],
            }),
        ) == ttorch.tensor({
            'a': [[True, False], [True, True]],
            'b': [True, False, True],
        })).all()

    def test_gt(self):
        assert (ttorch.gt(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[1, 1], [4, 4]]),
        ) == torch.tensor([[False, True],
                           [False, False]])).all()

        assert (ttorch.gt(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': [1.0, 1.5, 2.0],
            }),
            ttorch.tensor({
                'a': [[1, 1], [4, 4]],
                'b': [1.3, 1.2, 2.0],
            }),
        ) == ttorch.tensor({
            'a': [[False, True], [False, False]],
            'b': [False, True, False],
        })).all()

    def test_ge(self):
        assert (ttorch.ge(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[1, 1], [4, 4]]),
        ) == torch.tensor([[True, True],
                           [False, True]])).all()

        assert (ttorch.ge(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': [1.0, 1.5, 2.0],
            }),
            ttorch.tensor({
                'a': [[1, 1], [4, 4]],
                'b': [1.3, 1.2, 2.0],
            }),
        ) == ttorch.tensor({
            'a': [[True, True], [False, True]],
            'b': [False, True, True],
        })).all()

    def test_equal(self):
        p1 = ttorch.equal(torch.tensor([1, 2, 3]), torch.tensor([1, 2, 3]))
        assert isinstance(p1, bool)
        assert p1

        p2 = ttorch.equal(torch.tensor([1, 2, 3]), torch.tensor([1, 2, 4]))
        assert isinstance(p2, bool)
        assert not p2

        p3 = ttorch.equal({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 6]),
        }, ({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 6]),
        }))
        assert isinstance(p3, bool)
        assert p3

        p4 = ttorch.equal({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 6]),
        }, ({
            'a': torch.tensor([1, 2, 3]),
            'b': torch.tensor([4, 5, 5]),
        }))
        assert isinstance(p4, bool)
        assert not p4

    def test_min(self):
        t1 = ttorch.min(torch.tensor([1.0, 2.0, 1.5]))
        assert isinstance(t1, torch.Tensor)
        assert t1 == torch.tensor(1.0)

        assert ttorch.min(ttorch.tensor({
            'a': [1.0, 2.0, 1.5],
            'b': {'x': [[1.8, 0.9], [1.3, 2.5]]},
        })) == ttorch.tensor({
            'a': 1.0,
            'b': {'x': 0.9},
        })

    def test_max(self):
        t1 = ttorch.max(torch.tensor([1.0, 2.0, 1.5]))
        assert isinstance(t1, torch.Tensor)
        assert t1 == torch.tensor(2.0)

        assert ttorch.max(ttorch.tensor({
            'a': [1.0, 2.0, 1.5],
            'b': {'x': [[1.8, 0.9], [1.3, 2.5]]},
        })) == ttorch.tensor({
            'a': 2.0,
            'b': {'x': 2.5, }
        })

    def test_sum(self):
        assert ttorch.sum(torch.tensor([1.0, 2.0, 1.5])) == torch.tensor(4.5)
        assert ttorch.sum(ttorch.tensor({
            'a': [1.0, 2.0, 1.5],
            'b': {'x': [[1.8, 0.9], [1.3, 2.5]]},
        })) == torch.tensor(11.0)

    def test_clone(self):
        t1 = ttorch.clone(torch.tensor([1.0, 2.0, 1.5]))
        assert isinstance(t1, torch.Tensor)
        assert (t1 == torch.tensor([1.0, 2.0, 1.5])).all()

        t2 = ttorch.clone(ttorch.tensor({
            'a': [1.0, 2.0, 1.5],
            'b': {'x': [[1.8, 0.9], [1.3, 2.5]]},
        }))
        assert (t2 == ttorch.tensor({
            'a': [1.0, 2.0, 1.5],
            'b': {'x': [[1.8, 0.9], [1.3, 2.5]]},
        })).all()

    def test_dot(self):
        t1 = ttorch.dot(torch.tensor([1, 2]), torch.tensor([2, 3]))
        assert isinstance(t1, torch.Tensor)
        assert t1.tolist() == 8

        t2 = ttorch.dot(
            ttorch.tensor({
                'a': [1, 2, 3],
                'b': {'x': [3, 4]},
            }),
            ttorch.tensor({
                'a': [5, 6, 7],
                'b': {'x': [1, 2]},
            })
        )
        assert (t2 == ttorch.tensor({'a': 38, 'b': {'x': 11}})).all()

    def test_matmul(self):
        t1 = ttorch.matmul(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[5, 6], [7, 2]]),
        )
        assert isinstance(t1, torch.Tensor)
        assert (t1 == torch.tensor([[19, 10], [43, 26]])).all()

        t2 = ttorch.matmul(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': {'x': [3, 4, 5, 6]},
            }),
            ttorch.tensor({
                'a': [[5, 6], [7, 2]],
                'b': {'x': [4, 3, 2, 1]},
            }),
        )
        assert (t2 == ttorch.tensor({
            'a': [[19, 10], [43, 26]],
            'b': {'x': 40}
        })).all()

    def test_mm(self):
        t1 = ttorch.mm(
            torch.tensor([[1, 2], [3, 4]]),
            torch.tensor([[5, 6], [7, 2]]),
        )
        assert isinstance(t1, torch.Tensor)
        assert (t1 == torch.tensor([[19, 10], [43, 26]])).all()

        t2 = ttorch.mm(
            ttorch.tensor({
                'a': [[1, 2], [3, 4]],
                'b': {'x': [[3, 4, 5], [6, 7, 8]]},
            }),
            ttorch.tensor({
                'a': [[5, 6], [7, 2]],
                'b': {'x': [[6, 5], [4, 3], [2, 1]]},
            }),
        )
        assert (t2 == ttorch.tensor({
            'a': [[19, 10], [43, 26]],
            'b': {'x': [[44, 32], [80, 59]]},
        })).all()
